# -*- coding: utf-8 -*-

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.validation import V_REQUIRED
from Products.Archetypes.atapi import FileField
from Products.Archetypes.atapi import FileWidget
from Products.Archetypes.atapi import ImageField
from Products.Archetypes.atapi import ImageWidget
from Products.Archetypes.atapi import AnnotationStorage

def get_file_field():
     return FileField('file',
               required=True,
               primary=True,
               searchable=True,
               languageIndependent=True,
               storage = AnnotationStorage(migrate=True),
               validators = (('isNonEmptyFile', V_REQUIRED),
                              ('checkFileMaxSize', V_REQUIRED)),
               widget = FileWidget(
                         description = '',
                         label='File',
                         show_content_type = False,
               )
            )

def get_image_field():
    return ImageField('image',
                required=True,
                primary=True,
                languageIndependent=True,
                storage = AnnotationStorage(migrate=True),
                max_size = 10.0,
                maxsize = 10.0,  # The validator is searching on field for maxsize
                sizes= {'large'   : (768, 768),
                        'preview' : (400, 400),
                        'mini'    : (200, 200),
                        'thumb'   : (128, 128),
                        'tile'    :  (64, 64),
                        'icon'    :  (32, 32),
                        'listing' :  (16, 16),
                       },
                validators = (('isNonEmptyFile', V_REQUIRED),
                              ('checkImageMaxSize', V_REQUIRED)),
                widget = ImageWidget(
                         description = '',
                         label= u'Image',
                         show_content_type = False,)
         )


class PFObject(object):

    def getMaxSizeFor(self, name):
        return 20.0

@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    import plone.app.registry
    zcml.load_config('configure.zcml', plone.app.registry)
    fiveconfigure.debug_mode = False

setup_product()
ptc.setupPloneSite(products=['plone.app.registry'])


class NotInstalledTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit
    test cases.
    """
