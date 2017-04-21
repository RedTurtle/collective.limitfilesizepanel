# -*- coding: utf-8 -*-
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.interfaces import TypesSettings
from plone.registry.interfaces import IRegistry
from collective.limitfilesizepanel.tests import base
from collective.limitfilesizepanel.tests.base_dx import ITestSchema, FileObject, ImageObject, NewsObject
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.validation.validators.SupplValidators import MaxSizeValidator
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_INTEGRATION_TESTING  # noqa
from unittest import TestSuite, makeSuite
from zope.component import createObject
from zope.component import queryUtility
import unittest
from collective.limitfilesizepanel.dx_validators import DXFileSizeValidator
from plone.namedfile.field import NamedBlobFile


class TestMaxSizeCalcDX(unittest.TestCase):

    layer = LIMITFILESIZEPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.helper_view = api.content.get_view(
            name='lfsp_helpers_view',
            context=self.portal,
            request=self.portal.REQUEST,
        )
        self.registry = queryUtility(IRegistry)
        self.settings = self.registry.forInterface(ILimitFileSizePanel,
                                                   check=False)

    def test_size_file_dx_from_registry(self):
        # original validator for file and image read maxsize from
        # zconf.ATFile.max_file_size at the end we have a number
        # so we pass maxsize=N.
        # By default in the registry we have 30MB for file and 10MB for images
        # and calling the validator with all the possible values, validation
        # should be done with user values

        validator = DXFileSizeValidator(
            None,
            None,
            FileObject(),
            ITestSchema['file'],
            None
        )
        self.assertEqual(float(30), self.helper_view.get_maxsize_dx(
            validator,
            ITestSchema['file'])
        )

    def test_size_image_dx_from_registry(self):
        # original validator for file and image read maxsize from
        # zconf.ATFile.max_file_size at the end we have a number
        # so we pass maxsize=N.
        # By default in the registry we have 30MB for file and 10MB for images
        # and calling the validator with all the possible values, validation
        # should be done with user values

        validator = DXFileSizeValidator(
            None,
            None,
            ImageObject(),
            ITestSchema['image'],
            None
        )
        self.assertEqual(float(10), self.helper_view.get_maxsize_dx(
            validator,
            ITestSchema['image'])
        )

    def test_size_from_registry_type_setting_dx(self):
        validator = DXFileSizeValidator(
            None,
            None,
            NewsObject(),
            ITestSchema['image'],
            None
        )
        new_value = (TypesSettings(u'News Item', u'image', 7), )
        self.settings.types_settings += new_value
        self.assertEqual(
            float(7),
            self.helper_view.get_maxsize_dx(
                validator,
                ITestSchema['image'])
            )
        self.settings.types_settings = ()
