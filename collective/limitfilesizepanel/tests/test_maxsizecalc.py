# -*- coding: utf-8 -*-
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.interfaces import TypesSettings
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_INTEGRATION_TESTING  # NOQA
from collective.limitfilesizepanel.tests import base
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from Products.validation.validators.SupplValidators import MaxSizeValidator
from zope.component import queryUtility
import unittest


class TestMaxSizeCalc(unittest.TestCase):

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

    def test_size_from_registry(self):
        # original validator for file and image read maxsize from
        # zconf.ATFile.max_file_size at the end we have a number
        # so we pass maxsize=N.
        # By default in the registry we have 30MB for file and 10MB for images
        # and calling the validator with all the possible values, validation
        # should be done with user values
        validator = MaxSizeValidator('checkFileMaxSize', maxsize=50.0)
        self.assertEqual(float(30), self.helper_view.get_maxsize(
            validator,
            **{'maxsize': 15.0,
               'field': base.get_file_field(),
               'instance': base.PFObject()}
            )
        )
        self.assertEqual(float(10), self.helper_view.get_maxsize(
            validator,
            **{'maxsize': 15.0,
               'field': base.get_image_field(),
               'instance': base.PFObject()}
            )
        )

    def test_size_from_registry_type_setting(self):
        # new in version 1.3: type/field specific settings
        validator = MaxSizeValidator('checkFileMaxSize', maxsize=50.0)
        new_value = (TypesSettings(u'News Item', u'image', 7), )
        self.settings.types_settings += new_value
        self.assertEqual(
            float(7),
            self.helper_view.get_maxsize(
                validator,
                **{'maxsize': 15.0,
                   'field': base.get_image_field(),
                   'instance': base.PFObject()}
                )
            )
        self.settings.types_settings = ()

    def test_size_from_validator_instance(self):
        # original validator for file and image read maxsize from
        # zconf.ATFile.max_file_size at the end we have a number
        # By default in the registry we have 30MB for file and 10MB for images
        validator = MaxSizeValidator('checkFileMaxSize', maxsize=50.0)
        or_file_size = self.settings.file_size
        self.settings.file_size = 0
        self.assertEqual(float(50), self.helper_view.get_maxsize(
            validator,
            **{'field': base.get_file_field()}))
        self.settings.file_size = or_file_size

    def test_size_in_kwargs(self):
        validator = MaxSizeValidator('checkFileMaxSize')
        or_file_size = self.settings.file_size
        self.settings.file_size = 0
        self.assertEqual(
            float(15),
            self.helper_view.get_maxsize(
                validator,
                **{'maxsize': 15.0,
                   'field': base.get_file_field(),
                   'instance': base.PFObject()}
                )
            )
        self.settings.file_size = or_file_size

    def test_size_in_instance(self):
        validator = MaxSizeValidator('checkFileMaxSize')
        or_file_size = self.settings.file_size
        self.settings.file_size = 0
        self.assertEqual(
            float(20),
            self.helper_view.get_maxsize(
                validator,
                **{'field': base.get_file_field(),
                   'instance': base.PFObject()}
                )
            )
        self.settings.file_size = or_file_size

    def test_size_in_field(self):
        validator = MaxSizeValidator('checkFileMaxSize')
        or_image_size = self.settings.image_size
        self.settings.image_size = 0
        self.assertEqual(
            float(10),
            self.helper_view.get_maxsize(
                validator,
                **{'field': base.get_image_field()}
                )
            )
        self.settings.image_size = or_image_size

    def test_maxsize_file_for_tinymce(self):
        self.assertEqual(
            float(30),
            self.helper_view.get_maxsize_tiny(
                ['File']
                )
            )

    def test_maxsize_image_for_tinymce(self):
        self.assertEqual(
            float(10),
            self.helper_view.get_maxsize_tiny(
                ['Image']
                )
            )
