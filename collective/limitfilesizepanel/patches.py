# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Acquisition import aq_base
from Products.validation.i18n import recursiveTranslate
from Products.validation.i18n import safe_unicode
from ZPublisher.HTTPRequest import FileUpload
from collective.limitfilesizepanel import messageFactory as _
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility


def _get_type_maxsize(settings, instance, field):
    """Get portal_type/fieldname pair configuration in the registry"""
    portal_type = getattr(instance, 'portal_type')
    field_name = field.getName()
    for entry in settings.types_settings:
        if entry.content_type==portal_type and entry.field_name==field_name:
            return entry.size
    return None


def get_maxsize(validator, settings, **kwargs):
    # This is the patch:
    # * try to get sizes from plone.registry
    # * * if we find a type/field specific size: use it
    # * * if we have general sizes defined from user: use it
    # * if not, use the original method to calculate maxsize
    field = kwargs.get('field', None)
    instance = kwargs.get('instance', None)

    file_size, img_size = settings.file_size, settings.image_size

    # Check if there's a type/field specific settings in the registry
    if instance is not None:
        type_maxsize = _get_type_maxsize(settings, instance, field)
        if type_maxsize is not None:
            return type_maxsize

    # In plone 3 we have field.type == image/file
    # In plone 4 we have field.type == blob in both case
    # so:
    field_type = field.widget.__class__.__name__
    if field and file_size and field_type == 'FileWidget':
        maxsize = float(file_size)
    elif field and img_size and field_type == 'ImageWidget':
        maxsize = float(img_size)
    else:
        # get original max size
        if kwargs.has_key('maxsize'):
            maxsize = kwargs.get('maxsize')
        elif hasattr(aq_base(instance), 'getMaxSizeFor'):
            maxsize = instance.getMaxSizeFor(field.getName())
        elif hasattr(field, 'maxsize'):
            maxsize = field.maxsize
        else:
            # set to given default value (default defaults to 0)
            maxsize = validator.maxsize
    return maxsize


def patched__call__(self, value, *args, **kwargs):
    if canBypassValidation(kwargs.get('instance', None)):
        return True
    registry = queryUtility(IRegistry)
    settings = None
    if registry:
        try:
            settings = registry.forInterface(ILimitFileSizePanel, check=True)
        except KeyError:
            pass

    if not settings:
        return self._old___call__(value, *args, **kwargs)

    maxsize = get_maxsize(self, settings, **kwargs)

    if not maxsize:
        return True
    # calculate size
    elif (isinstance(value, FileUpload) or isinstance(value, file) or
          hasattr(aq_base(value), 'tell')):
        value.seek(0, 2)  # eof
        size = value.tell()
        value.seek(0)
    elif not settings.new_data_only:
        # we want to validate already saved data. Let use the default Atchetypes validation method
        try:
            size = len(value)
        except TypeError:
            size = 0
    else:
        # We don't want to validate already saved data
        return True

    size = float(size)
    sizeMB = (size / (1024 * 1024))

    if sizeMB > maxsize:
        msg = _('validation_error',
                default=u"Validation failed. Uploaded data is too large: ${size}MB (max ${max}MB)",
                mapping={
                    'name': safe_unicode(self.name),
                    'size': safe_unicode("%.1f" % sizeMB),
                    'max': safe_unicode("%.1f" % maxsize)})
        return recursiveTranslate(msg, **kwargs)
    else:
        return True


def canBypassValidation(context):
    """
    Check if the user has bypass permission
    """
    if not context:
        return False
    sm = getSecurityManager()
    return sm.checkPermission("collective.limitfilesizepanel: Bypass limit size", context)
