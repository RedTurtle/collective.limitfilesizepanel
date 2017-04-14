# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.limitfilesizepanel is properly installed."""

    layer = LIMITFILESIZEPANEL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.limitfilesizepanel is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.limitfilesizepanel'))

    def test_browserlayer(self):
        """Test that ILimitFileSizePanelLayer is registered."""
        from collective.limitfilesizepanel.interfaces import \
            ILimitFileSizePanelLayer
        from plone.browserlayer import utils
        self.assertIn(ILimitFileSizePanelLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = LIMITFILESIZEPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.limitfilesizepanel'])

    def test_product_uninstalled(self):
        """Test if collective.limitfilesizepanel is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.limitfilesizepanel'))

    def test_browserlayer_removed(self):
        """Test that ILimitFileSizePanelLayer is removed."""
        from collective.limitfilesizepanel.interfaces import \
            ILimitFileSizePanelLayer
        from plone.browserlayer import utils
        self.assertNotIn(ILimitFileSizePanelLayer, utils.registered_layers())
