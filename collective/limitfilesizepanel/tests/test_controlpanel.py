from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_RESTAPI_TESTING
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from plone.testing.zope import Browser

import transaction
import unittest


class TestControlpanel(unittest.TestCase):

    layer = LIMITFILESIZEPANEL_RESTAPI_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

    def tearDown(self):
        api.portal.set_registry_record(
            "new_data_only", True, interface=ILimitFileSizePanel
        )
        transaction.commit()

    def test_controlpanel_listed(self):
        response = self.api_session.get("@controlpanels")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "limitfilesize-settings",
            [x["@id"].split("/")[-1] for x in response.json()],
        )

    def test_controlpanel_schema(self):
        response = self.api_session.get("@controlpanels/limitfilesize-settings")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(
            sorted(data["schema"]["properties"].keys()),
            ["file_size", "image_size", "new_data_only", "types_settings"],
        )
        self.assertNotIn("new_data_only", data["schema"]["required"])
        self.assertEqual(data["data"]["file_size"], 30)

    def test_controlpanel_update(self):
        response = self.api_session.patch(
            "@controlpanels/limitfilesize-settings",
            json={"file_size": 200, "new_data_only": False},
        )
        self.assertEqual(response.status_code, 204)
        transaction.commit()

        self.assertEqual(
            api.portal.get_registry_record("file_size", interface=ILimitFileSizePanel),
            200,
        )
        self.assertFalse(
            api.portal.get_registry_record(
                "new_data_only", interface=ILimitFileSizePanel
            )
        )

    def test_classic_form_can_uncheck_new_data_only(self):
        browser = Browser(self.app)
        browser.handleErrors = False
        browser.addHeader(
            "Authorization",
            "Basic {}:{}".format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )
        browser.open(self.portal_url + "/@@limitfilesize-settings")
        browser.getControl(name="form.widgets.new_data_only").value = []
        browser.getControl(name="form.buttons.save").click()

        self.assertNotIn("Required input is missing", browser.contents)
        transaction.begin()
        self.assertFalse(
            api.portal.get_registry_record(
                "new_data_only", interface=ILimitFileSizePanel
            )
        )
