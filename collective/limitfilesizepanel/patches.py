# -*- coding: utf-8 -*-
from collective.limitfilesizepanel import messageFactory as _
from plone import api
from Products.validation.i18n import recursiveTranslate
from Products.validation.i18n import safe_unicode
from plone.api.exc import InvalidParameterError


def patched__call__(self, value, *args, **kwargs):
    context = kwargs.get('instance', None)

    try:
        helper_view = api.content.get_view(
            name='lfsp_helpers_view',
            context=context,
            request=context.REQUEST,
        )

    except InvalidParameterError:
        #  the view is enabled only when the product is installed
        return

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
                default=u"Validation failed. Uploaded data is too large: ${size}MB (max ${max}MB)",  # NOQA
                mapping={
                    'size': safe_unicode("%.1f" % size_check.get('sizeMB')),
                    'max': safe_unicode("%.1f" % size_check.get('maxsize'))
                    })
        return recursiveTranslate(msg, **kwargs)
    return True
