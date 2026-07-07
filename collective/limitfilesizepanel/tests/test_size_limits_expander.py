from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_RESTAPI_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

from plone.restapi.testing import RelativeSession
import transaction
import unittest


class TestFileConstraintsExpander(unittest.TestCase):

    layer = LIMITFILESIZEPANEL_RESTAPI_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.request = self.layer["request"]

        setRoles(self.portal, TEST_USER_ID, ["Manager", "Editor", "Contributor"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        api.portal.set_registry_record(
            "file_size", 10240, interface=ILimitFileSizePanel
        )

        self.file_obj = api.content.create(
            container=self.portal,
            type="File",
            title="Test File",
            id="test-file",
        )

        transaction.commit()

    def tearDown(self):
        api.content.delete(obj=self.file_obj)
        transaction.commit()

    def test_expander_present_in_components(self):
        response = self.api_session.get("test-file")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("limit-sizes", data.get("@components", {}))

    def test_expander_returns_max_size(self):
        response = self.api_session.get("@limit-sizes")
        self.assertEqual(response.status_code, 200)

        data = response.json()["items"]

        self.assertIn("file_size_limit", data)
        self.assertEqual(data["file_size_limit"], 10240)

    def test_expander_max_size_reflects_registry_change(self):
        api.portal.set_registry_record(
            "file_size", 51200, interface=ILimitFileSizePanel
        )
        transaction.commit()

        response = self.api_session.get("@limit-sizes")
        self.assertEqual(response.status_code, 200)

        data = response.json()["items"]

        self.assertIn("file_size_limit", data)
        self.assertEqual(data["file_size_limit"], 51200)
