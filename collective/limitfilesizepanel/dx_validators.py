# -*- coding: utf-8 -*-
from plone.namedfile.interfaces import INamedBlobImageField
from plone.namedfile.interfaces import INamedBlobFileField
from zope.interface import Invalid
from z3c.form import validator
from plone import api
from plone.api.exc import InvalidParameterError
from plone.dexterity.browser.edit import DefaultEditForm


class DXFileSizeValidator(validator.FileUploadValidator):
    """
    This validator is registered for all image and file fields.
    """

    def validate(self, value):
        super(DXFileSizeValidator, self).validate(value)
        if not value:
            return True

        if isinstance(self.view, DefaultEditForm):
            return True
        try:
            helper_view = api.content.get_view(
                name='lfsp_helpers_view',
                context=self.context,
                request=self.context.REQUEST,
            )
        except InvalidParameterError:
            #  the view is enabled only when the product is installed
            return True
        if helper_view.newDataOnly() and isinstance(self.view, DefaultEditForm):  # noqa
            return True
        maxsize = helper_view.get_maxsize_dx(
            validator=self,
            field=self.field
        )
        if not maxsize:
            return True

        size_check = helper_view.check_size_dx(
            maxsize=maxsize,
            uploadfile=value)

        if size_check and not size_check.get('valid', False):
            raise Invalid(size_check.get('error', ''))
        return True


class ImageFileSizeValidator(DXFileSizeValidator):
    """ """


class FileSizeValidator(DXFileSizeValidator):
    """ """


validator.WidgetValidatorDiscriminators(ImageFileSizeValidator,
                                        field=INamedBlobImageField)

validator.WidgetValidatorDiscriminators(FileSizeValidator,
                                        field=INamedBlobFileField)
