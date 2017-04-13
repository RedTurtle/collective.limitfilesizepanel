# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Acquisition import aq_base
from Products.validation.i18n import recursiveTranslate
from ZPublisher.HTTPRequest import FileUpload
from collective.limitfilesizepanel import messageFactory as _
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from plone import api
from plone.api.exc import InvalidParameterError
from Products.Five.browser import BrowserView
from zope.interface import Interface
from zope.interface import implements


class IHelpersView(Interface):

    def checkSize(uploadfile, maxsize):
        """ check the size of given file """

    def canBypassValidation():
        """Check if the user has bypass permission"""

    def get_maxsize(validator, field, **kwargs):
        """
        This is the method called from AT validator
        * try to get sizes from plone.registry
        * * if we find a type/field specific size: use it
        * * if we have general sizes defined from user: use it
        * if not, use the original method to calculate maxsize
        """

    def get_maxsize_tiny(metatypes):
        """
        Method for tinymce integration.
        Return max size set in the controlpanel.
        We manage only File and Image types because with tiny you can create
        only an image or a file.
        """


class View(BrowserView):
    '''
    Helper view for file uploads
    '''
    implements(IHelpersView)

    def check_size(self, uploadfile, maxsize):
        """ check the size of given file """
        result = {
            'maxsize': maxsize,
            'valid': True
        }

        if self.canBypassValidation():
            return result

        new_data_only = api.portal.get_registry_record(
            'new_data_only',
            interface=ILimitFileSizePanel)

        # calculate size
        if (isinstance(uploadfile, FileUpload) or isinstance(uploadfile, file) or
              hasattr(aq_base(uploadfile), 'tell')):
            uploadfile.seek(0, 2)  # eof
            size = uploadfile.tell()
            uploadfile.seek(0)
        elif not new_data_only:
            # we want to validate already saved data. Let use the default Atchetypes validation method
            try:
                size = len(uploadfile)
            except TypeError:
                size = 0
        else:
            # We don't want to validate already saved data
            return result

        size = float(size)
        sizeMB = (size / (1024 * 1024))
        result['sizeMB'] = sizeMB

        if sizeMB > maxsize:
            result['valid'] = False
        return result

    def canBypassValidation(self):
        """Check if the user has bypass permission"""

        sm = getSecurityManager()
        return sm.checkPermission(
            "collective.limitfilesizepanel: Bypass limit size", self.context)

    def _get_type_maxsize(self, field, context):
        """Get portal_type/fieldname pair configuration in the registry"""
        portal_type = getattr(context, 'portal_type')
        field_name = field.getName()
        types_settings = api.portal.get_registry_record(
            'types_settings',
            interface=ILimitFileSizePanel)
        for entry in types_settings:
            if entry.content_type == portal_type and entry.field_name == field_name:
                return entry.size
        return None

    def get_maxsize(self, validator, **kwargs):
        """
        This is the method called from AT validator
        * try to get sizes from plone.registry
        * * if we find a type/field specific size: use it
        * * if we have general sizes defined from user: use it
        * if not, use the original method to calculate maxsize
        """
        context = self.context
        field = kwargs.get('field', None)
        instance = kwargs.get('instance', None)
        if instance:
            context = instance
        try:
            file_size = api.portal.get_registry_record(
                'file_size',
                interface=ILimitFileSizePanel)
            image_size = api.portal.get_registry_record(
                'image_size',
                interface=ILimitFileSizePanel)
        except InvalidParameterError:
            return None
        # Check if there's a type/field specific settings in the registry
        type_maxsize = self._get_type_maxsize(field, context)
        if type_maxsize is not None:
            return type_maxsize

        # In plone 3 we have field.type == image/file
        # In plone 4 we have field.type == blob in both case
        # so:
        field_type = field.widget.__class__.__name__
        if field and file_size and field_type == 'FileWidget':
            maxsize = float(file_size)
        elif field and image_size and field_type == 'ImageWidget':
            maxsize = float(image_size)
        else:
            # get original max size
            if 'maxsize' in kwargs:
                maxsize = kwargs.get('maxsize')
            elif hasattr(aq_base(instance), 'getMaxSizeFor'):
                maxsize = instance.getMaxSizeFor(field.getName())
            elif hasattr(field, 'maxsize'):
                maxsize = field.maxsize
            else:
                # set to given default value (default defaults to 0)
                maxsize = validator.maxsize
        return maxsize

    def get_maxsize_tiny(self, metatypes):
        """
        Method for tinymce integration.
        Return max size set in the controlpanel.
        We manage only File and Image types because with tiny you can create
        only an image or a file.
        """
        if len(metatypes) != 1:
            return 0
        file_size = api.portal.get_registry_record(
            'file_size',
            interface=ILimitFileSizePanel)
        image_size = api.portal.get_registry_record(
            'image_size',
            interface=ILimitFileSizePanel)
        if metatypes[0] == 'File' and file_size:
            return float(file_size)
        elif metatypes[0] == 'Image' and image_size:
            return float(image_size)
        return 0
