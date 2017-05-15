# -*- coding: utf-8 -*-
from Products.validation.i18n import safe_unicode
from plone.namedfile.interfaces import INamedBlobImageField
from plone.namedfile.interfaces import INamedBlobFileField
from collective.limitfilesizepanel import messageFactory as _
from zope.interface import Invalid
from z3c.form import validator
from plone import api
from plone.api.exc import InvalidParameterError
from zope.i18n import translate


class DXFileSizeValidator(validator.FileUploadValidator):
    """
    This validator is registered for all image and file fields.
    """

    def validate(self, value):
        super(DXFileSizeValidator, self).validate(value)
        if not value:
            return
        try:
            helper_view = api.content.get_view(
                name='lfsp_helpers_view',
                context=self.context,
                request=self.context.REQUEST,
            )
        except InvalidParameterError:
            #  the view is enabled only when the product is installed
            return
        if helper_view.canBypassValidation():
            return True
        maxsize = helper_view.get_maxsize_dx(self, self.field)
        if not maxsize:
            return True

        size_check = helper_view.check_size_dx(
            maxsize=maxsize,
            uploadfile=value)

        if size_check and not size_check.get('valid', False):
            msg = _(
                'validation_error',
                default=u"Validation failed. Uploaded data is too large:"
                        u" ${size}MB (max ${max}MB)",
                mapping={
                    'size': safe_unicode("%.1f" % size_check.get('sizeMB')),
                    'max': safe_unicode("%.1f" % size_check.get('maxsize'))
                })
            raise Invalid(translate(msg, context=self.context.REQUEST))
        return True


validator.WidgetValidatorDiscriminators(DXFileSizeValidator,
                                        field=INamedBlobImageField)

validator.WidgetValidatorDiscriminators(DXFileSizeValidator,
                                        field=INamedBlobFileField)
