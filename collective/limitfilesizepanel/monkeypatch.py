# -*- coding: utf-8 -*-

from Acquisition import aq_base
from Products.validation.i18n import PloneMessageFactory as _
from Products.validation.i18n import recursiveTranslate
from Products.validation.i18n import safe_unicode
from Products.validation.validators.SupplValidators import MaxSizeValidator
from ZPublisher.HTTPRequest import FileUpload
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility

from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel


def get_user_file_limit():
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(ILimitFileSizePanel, check=False)
    return settings.file_size, settings.image_size


def get_maxsize(validator, **kwargs):
    #This is the patch:
    # * try to get sizes from plone.registry
    # * if we have sizes defined from user use it
    # * if not, use the original method to calculate maxsize
    file_size, img_size = get_user_file_limit()
    if file_size and field.type == 'file':
        maxsize = float(file_size)
    elif img_size and field.type == 'image':
        maxsize = float(img_size)
    else:
        instance = kwargs.get('instance', None)
        field = kwargs.get('field', None)
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


def patched__call__(self, value, *args, **kwargs):

    maxsize = get_maxsize(self, **kwargs)

    if not maxsize:
        return True

    # calculate size
    elif (isinstance(value, FileUpload) or isinstance(value, file) or
          hasattr(aq_base(value), 'tell')):
        value.seek(0, 2)  # eof
        size = value.tell()
        value.seek(0)
    else:
        try:
            size = len(value)
        except TypeError:
            size = 0
    size = float(size)
    sizeMB = (size / (1024 * 1024))

    if sizeMB > maxsize:
        msg = _("Validation failed($name: Uploaded data is too large: ${size}MB (max ${max}MB)",
                mapping={
                    'name': safe_unicode(self.name),
                    'size': safe_unicode("%.3f" % sizeMB),
                    'max': safe_unicode("%.3f" % maxsize)})
        return recursiveTranslate(msg, **kwargs)
    else:
        return True

MaxSizeValidator.__call__ = patched__call__
