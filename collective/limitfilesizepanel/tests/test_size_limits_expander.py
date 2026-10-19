from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import transaction
import unittest


EXPOSE_PERMISSION = "collective.limitfilesizepanel: Expose size limits"
BYPASS_PERMISSION = "collective.limitfilesizepanel: Bypass limit size"


class TestSizeLimits(unittest.TestCase):

    layer = LIMITFILESIZEPANEL_RESTAPI_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        api.user.create(
            email="manager@example.com",
            username="manager",
            password="secret!!",
            roles=["Manager"],
        )
        api.user.create(
            email="editor@example.com",
            username="editor",
            password="secret!!",
            roles=["Editor"],
        )
        api.user.create(
            email="member@example.com",
            username="member",
            password="secret!!",
            roles=["Member"],
        )
        api.portal.set_registry_record("file_size", 50, interface=ILimitFileSizePanel)
        api.portal.set_registry_record("image_size", 5, interface=ILimitFileSizePanel)
        self.folder = api.content.create(
            container=self.portal,
            type="Folder",
            title="Folder",
            id="folder",
        )
        api.content.transition(obj=self.folder, transition="publish")
        transaction.commit()

    def tearDown(self):
        api.content.delete(obj=self.folder)
        for username in ["manager", "editor", "member"]:
            api.user.delete(username=username)
        transaction.commit()

    def session(self, auth=None):
        session = RelativeSession(self.portal_url)
        session.headers.update({"Accept": "application/json"})
        if auth:
            session.auth = auth
        return session

    def test_expander_present_in_components(self):
        response = self.session().get("folder")
        self.assertEqual(response.status_code, 200)

        components = response.json()["@components"]
        self.assertIn("limit-sizes", components)
        self.assertEqual(
            components["limit-sizes"],
            {"@id": "{}/folder/@limit-sizes".format(self.portal_url)},
        )

    def test_service_returns_limits(self):
        response = self.session(auth=("editor", "secret!!")).get("@limit-sizes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["items"],
            {"file_size_limit": 50, "image_size_limit": 5, "can_bypass": False},
        )

    def test_service_reflects_registry_change(self):
        api.portal.set_registry_record("file_size", 0, interface=ILimitFileSizePanel)
        transaction.commit()

        response = self.session(auth=("editor", "secret!!")).get("@limit-sizes")
        self.assertEqual(response.json()["items"]["file_size_limit"], 0)

    def test_service_allowed_for_manager(self):
        response = self.session(auth=("manager", "secret!!")).get("@limit-sizes")
        self.assertEqual(response.status_code, 200)

    def test_service_allowed_for_site_owner(self):
        response = self.session(auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD)).get(
            "@limit-sizes"
        )
        self.assertEqual(response.status_code, 200)

    def test_service_unauthorized_for_member_and_anonymous(self):
        response = self.session(auth=("member", "secret!!")).get("@limit-sizes")
        self.assertEqual(response.status_code, 401)
        response = self.session().get("@limit-sizes")
        self.assertEqual(response.status_code, 401)

    def test_service_uses_local_roles(self):
        api.user.grant_roles(username="member", obj=self.folder, roles=["Contributor"])
        transaction.commit()

        session = self.session(auth=("member", "secret!!"))
        self.assertEqual(session.get("@limit-sizes").status_code, 401)
        self.assertEqual(session.get("folder/@limit-sizes").status_code, 200)

    def test_expanded_returns_limits_for_editor(self):
        response = self.session(auth=("editor", "secret!!")).get(
            "folder?expand=limit-sizes"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()["@components"]["limit-sizes"]
        self.assertEqual(
            data["items"],
            {"file_size_limit": 50, "image_size_limit": 5, "can_bypass": False},
        )

    def test_expanded_hides_limits_without_permission(self):
        response = self.session().get("folder?expand=limit-sizes")
        self.assertEqual(response.status_code, 200)
        data = response.json()["@components"]["limit-sizes"]
        self.assertNotIn("items", data)

        response = self.session(auth=("member", "secret!!")).get(
            "folder?expand=limit-sizes"
        )
        data = response.json()["@components"]["limit-sizes"]
        self.assertNotIn("items", data)

    def test_can_bypass(self):
        self.portal.manage_permission(
            BYPASS_PERMISSION, roles=["Editor"], acquire=False
        )
        transaction.commit()

        response = self.session(auth=("editor", "secret!!")).get("@limit-sizes")
        self.assertTrue(response.json()["items"]["can_bypass"])

    def test_upgrade_to_1400_sets_permission_roles(self):
        from collective.limitfilesizepanel.setuphandlers import migrateTo1400

        self.portal.manage_permission(EXPOSE_PERMISSION, roles=[], acquire=False)
        migrateTo1400(self.portal)

        roles = [
            r["name"]
            for r in self.portal.rolesOfPermission(EXPOSE_PERMISSION)
            if r["selected"]
        ]
        self.assertEqual(
            sorted(roles),
            ["Contributor", "Editor", "Manager", "Site Administrator"],
        )
