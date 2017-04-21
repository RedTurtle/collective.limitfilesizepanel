# -*- coding: utf-8 -*-
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_INTEGRATION_TESTING  # NOQA
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
import unittest


class TestBypassSize(unittest.TestCase):
    """
    This test cover the bypass size validation feature.
    """

    layer = LIMITFILESIZEPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.helper_view = api.content.get_view(
            name='lfsp_helpers_view',
            context=self.portal,
            request=self.portal.REQUEST,
        )

    def test_bypass_validation(self):
        """
        """
        # first check that current user can't bypass validation
        self.assertFalse(self.helper_view.canBypassValidation())
        # now set the permission to "Member" role
        self.portal.manage_permission(
            'collective.limitfilesizepanel: Bypass limit size',
            ['Member'],
            acquire=False)
        # now check that current user can bypass validation
        self.assertTrue(self.helper_view.canBypassValidation())

    def tearDown(self):
        """
        revert settings to default
        """
        self.portal.manage_permission(
            'collective.limitfilesizepanel: Bypass limit size',
            [],
            acquire=False)
