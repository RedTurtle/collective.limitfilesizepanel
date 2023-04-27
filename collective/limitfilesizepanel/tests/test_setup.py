# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.limitfilesizepanel.testing import (
    LIMITFILESIZEPANEL_INTEGRATION_TESTING,
)  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.limitfilesizepanel is properly installed."""

    layer = LIMITFILESIZEPANEL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if collective.limitfilesizepanel is installed."""
        self.assertTrue(
            self.installer.isProductInstalled("collective.limitfilesizepanel")
        )

    def test_browserlayer(self):
        """Test that ILimitFileSizePanelLayer is registered."""
        from collective.limitfilesizepanel.interfaces import ILimitFileSizePanelLayer
        from plone.browserlayer import utils

        self.assertIn(ILimitFileSizePanelLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    layer = LIMITFILESIZEPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["collective.limitfilesizepanel"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.limitfilesizepanel is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled("collective.limitfilesizepanel")
        )

    def test_browserlayer_removed(self):
        """Test that ILimitFileSizePanelLayer is removed."""
        from collective.limitfilesizepanel.interfaces import ILimitFileSizePanelLayer
        from plone.browserlayer import utils

        self.assertNotIn(ILimitFileSizePanelLayer, utils.registered_layers())
