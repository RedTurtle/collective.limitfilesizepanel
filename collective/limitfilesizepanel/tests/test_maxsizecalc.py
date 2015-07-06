# -*- coding: utf-8 -*-

from Products.validation.validators.SupplValidators import MaxSizeValidator
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.interfaces import TypesSettings
from collective.limitfilesizepanel.patches import get_maxsize
from collective.limitfilesizepanel.tests import base
from plone.registry.interfaces import IRegistry
from unittest import TestSuite, makeSuite
from zope.component import queryUtility


class TestMaxSizeCalc(base.MaxSizeTestCase):
    """
    This test cover the file/image size validation monkeypatch.
    File/Image AT validates using zconf.ATFile.max_file_size, so we
    check only this case
    """

    def afterSetUp(self):
        """
        nothing to do here
        """
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
        self.assertEqual(float(30), get_maxsize(validator,
                                                self.settings,
                                                **{'maxsize': 15.0 ,
                                                   'field': base.get_file_field(),
                                                   'instance': base.PFObject()
                                                  }
                                    )
                                  )
        self.assertEqual(float(10), get_maxsize(validator,
                                                self.settings,
                                                **{'maxsize': 15.0 ,
                                                   'field': base.get_image_field(),
                                                   'instance': base.PFObject()
                                                  }
                                    )
                                 )

    def test_size_from_registry_type_setting(self):
        # new in version 1.3: type/field specific settings
        validator = MaxSizeValidator('checkFileMaxSize', maxsize=50.0)
        self.settings.types_settings += (TypesSettings(u'News Item', u'image', 7), )
        self.assertEqual(float(7),
                         get_maxsize(validator,
                                     self.settings,
                                     **{'maxsize': 15.0 ,
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
        self.assertEqual(float(50), get_maxsize(validator,
                                                self.settings,
                                                **{'field': base.get_file_field()} ))
        self.settings.file_size = or_file_size

    def test_size_in_kwargs(self):
        validator = MaxSizeValidator('checkFileMaxSize')
        or_file_size = self.settings.file_size
        self.settings.file_size = 0
        self.assertEqual(float(15),
                         get_maxsize(validator,
                                     self.settings,
                                     **{'maxsize': 15.0 ,
                                        'field': base.get_file_field(),
                                        'instance': base.PFObject()}
                                     )
                         )
        self.settings.file_size = or_file_size

    def test_size_in_instance(self):
        validator = MaxSizeValidator('checkFileMaxSize')
        or_file_size = self.settings.file_size
        self.settings.file_size = 0
        self.assertEqual(float(20),
                         get_maxsize(validator,
                                     self.settings,
                                     **{'field': base.get_file_field(),
                                        'instance': base.PFObject()}
                                     )
                         )
        self.settings.file_size = or_file_size

    def test_size_in_field(self):
        validator = MaxSizeValidator('checkFileMaxSize')
        or_image_size = self.settings.image_size
        self.settings.image_size = 0
        self.assertEqual(float(10),
                         get_maxsize(validator,
                                     self.settings,
                                     **{'field': base.get_image_field()}
                                     )
                         )
        self.settings.image_size = or_image_size


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestMaxSizeCalc))
    return suite
