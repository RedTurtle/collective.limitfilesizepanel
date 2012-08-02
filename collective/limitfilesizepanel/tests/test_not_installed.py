# -*- coding: utf-8 -*-

from unittest import TestSuite, makeSuite
from zope.component import queryUtility
from Products.validation.validators.SupplValidators import MaxSizeValidator
from plone.registry.interfaces import IRegistry

from collective.limitfilesizepanel.tests import base_not_installed as base
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.monkeypatch import get_maxsize

class TestNotinstalled(base.NotInstalledTestCase):
    
    def test_registry(self):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ILimitFileSizePanel,
                                         check = False)
        self.assertEqual(None, settings.file_size)
        self.assertEqual(None, settings.image_size)
    
    def test_size_from_validator_instance(self):
        validator = MaxSizeValidator('checkFileMaxSize', maxsize=50.0)
        self.assertEqual(float(50), get_maxsize(validator,
                                        **{'field': base.get_file_field()}))

    def test_size_in_kwargs(self):
        validator = MaxSizeValidator('checkFileMaxSize')
        self.assertEqual(float(15),
                         get_maxsize(validator,
                                     **{'maxsize':15.0 ,
                                        'field': base.get_file_field(),
                                        'instance': base.PFObject()}
                                     )
                         )
    
    def test_size_in_instance(self):
        validator = MaxSizeValidator('checkFileMaxSize')
        self.assertEqual(float(20), 
                         get_maxsize(validator,
                                     **{'field': base.get_file_field(),
                                        'instance': base.PFObject()}
                                     )
                         )

    def test_size_in_field(self):
        validator = MaxSizeValidator('checkFileMaxSize')
        self.assertEqual(float(10),
                         get_maxsize(validator,
                                     **{'field': base.get_image_field()}
                                     )
                         )
    
def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestNotinstalled))
    return suite