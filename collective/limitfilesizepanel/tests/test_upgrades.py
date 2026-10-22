from collective.limitfilesizepanel.setuphandlers import migrateTo1400
from collective.limitfilesizepanel.setuphandlers import TYPES_SETTINGS_RECORD
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_INTEGRATION_TESTING
from collective.limitfilesizepanel.testing import (
    LIMITFILESIZEPANEL_JSONWIDGET_INTEGRATION_TESTING,
)
from plone import api
from plone.base.utils import get_installer
from plone.browserlayer import utils
from plone.registry import field
from plone.registry.record import Record

import unittest


class TestUpgradeTo1400(unittest.TestCase):
    layer = LIMITFILESIZEPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.registry = api.portal.get_tool("portal_registry")

    def test_removes_types_settings(self):
        self.registry.records[TYPES_SETTINGS_RECORD] = Record(field.SourceText(), "[]")
        migrateTo1400(self.portal)

        self.assertNotIn(TYPES_SETTINGS_RECORD, self.registry.records)
        # running it again does not break
        migrateTo1400(self.portal)

    def test_jsonwidget_not_installed(self):
        # jsonwidget zcml is not loaded here, so its profile is unknown
        migrateTo1400(self.portal)

        installer = get_installer(self.portal, self.layer["request"])
        self.assertFalse(
            installer.is_product_installed("collective.z3cform.jsonwidget")
        )


class TestUpgradeTo1400JSONWidget(unittest.TestCase):
    layer = LIMITFILESIZEPANEL_JSONWIDGET_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.registry = api.portal.get_tool("portal_registry")
        self.installer = get_installer(self.portal, self.request)

    def get_jsonwidget_records(self):
        return [
            name
            for name in self.registry.records.keys()
            if name.startswith("plone.bundles/z3cform-jsonwidget")
        ]

    def test_uninstalls_jsonwidget(self):
        from collective.z3cform.jsonwidget.interfaces import (
            ICollectiveZ3CformJsonwidgetLayer,
        )

        self.assertTrue(
            self.installer.is_product_installed("collective.z3cform.jsonwidget")
        )
        self.assertTrue(self.get_jsonwidget_records())

        migrateTo1400(self.portal)

        self.assertFalse(
            self.installer.is_product_installed("collective.z3cform.jsonwidget")
        )
        self.assertFalse(self.get_jsonwidget_records())
        self.assertNotIn(ICollectiveZ3CformJsonwidgetLayer, utils.registered_layers())
