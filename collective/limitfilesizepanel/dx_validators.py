# -*- coding: utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from plone.namedfile.interfaces import INamedFileField
from plone.namedfile.interfaces import IPluggableFileFieldValidation
from plone.namedfile.interfaces import IPluggableImageFieldValidation
from plone.namedfile.interfaces import INamedImageField
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.globalrequest import getRequest
from zope.schema import ValidationError


class InvalidSize(ValidationError):
    """Exception for invalid size"""

    __doc__ = "Invalid size"

    def doc(self):
        if len(self.args) > 1:
            return self.args[0]
        else:
            return self.__class__.__doc__


class BaseFileSizeValidator:
    """ """

    def __init__(self, field, value):
        self.field = field
        self.value = value
        self.request = getRequest()

    @property
    def helper_view(self):
        try:
            return api.content.get_view(
                name="lfsp_helpers_view",
                context=api.portal.get(),
                request=self.request,
            )
        except InvalidParameterError:
            return None

    def __call__(self):
        if not self.value:
            return True
        if not self.helper_view:
            #  the view is enabled only when the product is installed
            return True
        if self.skip():
            return True
        maxsize = self.helper_view.get_maxsize(
            field=self.field, portal_type=self.get_portal_type()
        )
        if not maxsize:
            return True

        size_check = self.helper_view.check_size(
            maxsize=maxsize,
            uploadfile=self.value,
        )

        if size_check and not size_check.get("valid", False):
            raise InvalidSize(size_check.get("error", ""), self.field.__name__)
        return True

    def skip(self):
        """
        Skip only if we are in edit mode and newDataOnly is set
        """
        if not self.helper_view.newDataOnly():
            return False

        if self.request.steps[-1].startswith("++add++"):
            return False
        if self.request.method != "PATCH":
            # restapi calls
            return False
        return True

    def get_portal_type(self):
        if self.request.steps:
            if self.request.steps[-1].startswith("++add++"):
                return self.request.steps[-1].replace("++add++", "")
            if "@type" in self.request.form:
                return self.request.form["@type"]
        return self.field.context.portal_type


@implementer(IPluggableFileFieldValidation)
@adapter(INamedFileField, Interface)
class FileSizeValidator(BaseFileSizeValidator):
    """plone.namedfiled validator for filetype"""


@implementer(IPluggableImageFieldValidation)
@adapter(INamedImageField, Interface)
class ImageSizeValidator(BaseFileSizeValidator):
    """plone.namedfiled validator for image"""
