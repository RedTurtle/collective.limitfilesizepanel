from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import PLONE_RESTAPI_DX_FUNCTIONAL_TESTING
import transaction
import unittest



class TestFileConstraintsExpander(unittest.TestCase):

    layer = PLONE_RESTAPI_DX_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.request = self.layer["request"]

        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        api.portal.set_registry_record('file_size', 10240, interface=ILimitFileSizePanel)

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

    def _get_response(self, url, expand=None):
        from requests import get
        from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

        if expand:
            url = f"{url}?expand={expand}"

        response = get(
            url,
            headers={"Accept": "application/json"},
            auth=(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        return response

    def test_expander_present_in_components(self):
        response = self._get_response(
            f"{self.portal_url}/test-file"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("limit-sizes", data.get("@components", {}))

    def test_expander_returns_max_size(self):
        response = self._get_response(
            f"{self.portal_url}/test-file",
            expand="limit-sizes",
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        component = data["@components"]["limit-sizes"]

        self.assertIn("file_size_limit", component)
        self.assertEqual(component["file_size_limit"], 10240)

    def test_expander_max_size_reflects_registry_change(self):
        api.portal.set_registry_record('file_size', 51200, interface=ILimitFileSizePanel)
        transaction.commit()

        response = self._get_response(
            f"{self.portal_url}/test-file",
            expand="limit-sizes",
        )
        data = response.json()
        component = data["@components"]["limit-sizes"]

        self.assertEqual(component["file_size_limit"], 51200)
