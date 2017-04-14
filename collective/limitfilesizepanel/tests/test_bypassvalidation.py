# -*- coding: utf-8 -*-
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.interfaces import TypesSettings
from plone.registry.interfaces import IRegistry
from collective.limitfilesizepanel.tests import base
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.validation.validators.SupplValidators import MaxSizeValidator
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_INTEGRATION_TESTING  # noqa
from unittest import TestSuite, makeSuite
from zope.component import createObject
from zope.component import queryUtility
import unittest


class TestBypassSize(unittest.TestCase):
    """
    This test cover the bypass size validation feature.
    """

    layer = LIMITFILESIZEPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
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
