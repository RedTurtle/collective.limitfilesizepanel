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
from plone import api


def patched__call__(self, value, *args, **kwargs):
    context = kwargs.get('instance', None)
    helper_view = api.content.get_view(
        name='lfsp_helpers_view',
        context=context,
        request=context.REQUEST,
    )

    if helper_view.canBypassValidation():
        return True

    maxsize = helper_view.get_maxsize(self, **kwargs)
    if not maxsize:
        return self._old___call__(value, *args, **kwargs)

    size_check = helper_view.check_size(
        maxsize=maxsize,
        uploadfile=value)

    if size_check and not size_check.get('valid', False):
        msg = _('validation_error',
                default=u"Validation failed. Uploaded data is too large: ${size}MB (max ${max}MB)",
                mapping={
                    'size': safe_unicode("%.1f" % size_check.get('sizeMB')),
                    'max': safe_unicode("%.1f" % size_check.get('maxsize'))
                    })
        return recursiveTranslate(msg, **kwargs)
    return True
