# -*- coding: utf-8 -*-
from Acquisition import aq_base
from collective.limitfilesizepanel import messageFactory as _
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from plone import api
from plone.api.exc import InvalidParameterError
from Products.Five.browser import BrowserView
from Products.validation.i18n import safe_unicode
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from ZPublisher.HTTPRequest import FileUpload

try:
    from plone.namedfile.interfaces import INamedBlobImageField
    from plone.namedfile.interfaces import INamedBlobFileField
    HAS_DX = True
except ImportError:
    HAS_DX = False


class IHelpersView(Interface):

    def checkSize(uploadfile, maxsize):
        """ check the size of given file """

    def canBypassValidation():
        """Check if the user has bypass permission"""

    def newDataOnly():
        """ Return if the validation is only for new data """

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


@implementer(IHelpersView)
class View(BrowserView):
    """
    Helper view for file uploads
    """

    def newDataOnly(self):
        """
        """
        return api.portal.get_registry_record(
            'new_data_only',
            interface=ILimitFileSizePanel)

    def check_size_dx(self, uploadfile, maxsize):
        """ check the size of given file """
        result = {
            'maxsize': maxsize,
            'valid': True
        }
        if self.canBypassValidation():
            return result
        if (isinstance(uploadfile, FileUpload) or hasattr(aq_base(uploadfile), 'tell')):  # NOQA
            uploadfile.seek(0, 2)  # eof
            size = float(uploadfile.tell())
            uploadfile.seek(0)
        else:
            size = float(uploadfile.getSize())
        sizeMB = (size / (1024 * 1024))
        result['sizeMB'] = sizeMB
        if sizeMB > maxsize:
            result['valid'] = False
            msg = _(
                'validation_error',
                default=u'Validation failed. Uploaded data is too large:'
                        u' ${size}MB (max ${max}MB)',
                mapping={
                    'size': safe_unicode('{0:.1f}'.format(sizeMB)),
                    'max': safe_unicode('{0:.1f}'.format(maxsize))
                })
            result['error'] = translate(msg, context=self.request)
        return result

    def check_size(self, uploadfile, maxsize):
        """ check the size of given file """
        result = {
            'maxsize': maxsize,
            'valid': True,
        }

        if self.canBypassValidation():
            return result

        new_data_only = api.portal.get_registry_record(
            'new_data_only',
            interface=ILimitFileSizePanel)
        # calculate size
        if (isinstance(uploadfile, FileUpload) or isinstance(uploadfile, file) or hasattr(aq_base(uploadfile), 'tell')):  # NOQA
            uploadfile.seek(0, 2)  # eof
            size = uploadfile.tell()
            uploadfile.seek(0)
        elif not new_data_only:
            # we want to validate already saved data. Let use the default
            # Archetypes validation method
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
            msg = _(
                'validation_error',
                default=u'Validation failed. Uploaded data is too large:'
                        u' ${size}MB (max ${max}MB)',
                mapping={
                    'size': safe_unicode('{0:.1f}'.format(sizeMB)),
                    'max': safe_unicode('{0:.1f}'.format(maxsize))
                })
            result['error'] = translate(msg, context=self.request)
        return result

    def canBypassValidation(self):
        """Check if the user has bypass permission"""

        return api.user.has_permission(
            'collective.limitfilesizepanel: Bypass limit size',
            obj=self.context
        )

    def _get_type_maxsize(self, field, context):
        """Get portal_type/fieldname pair configuration in the registry"""
        portal_type = getattr(context, 'portal_type', None)
        if not portal_type:
            return None
        field_name = field.getName()
        types_settings = api.portal.get_registry_record(
            'types_settings',
            interface=ILimitFileSizePanel)
        for entry in types_settings:
            ctype = entry.content_type
            cfield_name = entry.field_name
            if ctype == portal_type and cfield_name == field_name:
                return entry.size
        return None

    def get_maxsize_dx(self, validator, field):
        """
        """
        if not HAS_DX:
            return None
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
        type_context = self.context
        if self.context == api.portal.get():
            # we are in add form, so context is the portal.
            # validator.view has an attribute portal_type with the wanted type
            type_context = validator.view
        type_maxsize = self._get_type_maxsize(field, type_context)
        if type_maxsize is not None:
            return type_maxsize
        if file_size and INamedBlobFileField.providedBy(field):
            return float(file_size)
        elif image_size and INamedBlobImageField.providedBy(field):
            return float(image_size)
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
            elif hasattr(aq_base(instance), 'getMaxSizeFor'):  # noqa
                maxsize = instance.getMaxSizeFor(field.getName())
            elif hasattr(field, 'maxsize'):  # noqa
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
