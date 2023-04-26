# -*- coding: utf-8 -*-
from Acquisition import aq_base
from collective.limitfilesizepanel import messageFactory as _
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from plone import api
from plone.api.exc import InvalidParameterError
from Products.Five.browser import BrowserView
from Products.CMFPlone.utils import safe_unicode
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from ZPublisher.HTTPRequest import FileUpload
from plone.namedfile.interfaces import INamedImageField
from plone.namedfile.interfaces import INamedFileField

import json


class IHelpersView(Interface):
    def checkSize(uploadfile, maxsize):
        """check the size of given file"""

    def canBypassValidation():
        """Check if the user has bypass permission"""

    def newDataOnly():
        """Return if the validation is only for new data"""

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
        """ """
        return api.portal.get_registry_record(
            "new_data_only", interface=ILimitFileSizePanel
        )

    def check_size(self, uploadfile, maxsize):
        """check the size of given file"""
        result = {"maxsize": maxsize, "valid": True}
        if self.canBypassValidation():
            return result
        if isinstance(uploadfile, FileUpload) or hasattr(
            aq_base(uploadfile), "tell"
        ):  # NOQA
            uploadfile.seek(0, 2)  # eof
            size = float(uploadfile.tell())
            uploadfile.seek(0)
        else:
            size = float(uploadfile.getSize())
        sizeMB = size / (1024 * 1024)
        result["sizeMB"] = sizeMB
        if sizeMB > maxsize:
            result["valid"] = False
            msg = _(
                "validation_error",
                default=u"Validation failed. Uploaded data is too large:"
                u" ${size}MB (max ${max}MB)",
                mapping={
                    "size": safe_unicode("{0:.1f}".format(sizeMB)),
                    "max": safe_unicode("{0:.1f}".format(maxsize)),
                },
            )
            result["error"] = translate(msg, context=self.request)
        return result

    def canBypassValidation(self):
        """Check if the user has bypass permission"""

        return api.user.has_permission(
            "collective.limitfilesizepanel: Bypass limit size", obj=self.context
        )

    def _get_type_maxsize(self, field, portal_type):
        """Get portal_type/fieldname pair configuration in the registry"""
        if not portal_type:
            return None
        field_name = field.getName()
        types_settings = (
            api.portal.get_registry_record(
                "types_settings", interface=ILimitFileSizePanel
            )
            or "[]"  # noqa
        )
        types_settings = json.loads(types_settings)
        for entry in types_settings:
            ctype = entry.get("content_type", "")
            cfield_name = entry.get("field_name", "")
            if ctype == portal_type and cfield_name == field_name:
                size = entry.get("size", "")
                if size:
                    return float(size)
        return None

    def get_maxsize(self, field, portal_type=""):
        """ """
        try:
            file_size = api.portal.get_registry_record(
                "file_size", interface=ILimitFileSizePanel
            )
            image_size = api.portal.get_registry_record(
                "image_size", interface=ILimitFileSizePanel
            )
        except InvalidParameterError:
            return None
        # Check if there's a type/field specific settings in the registry
        type_maxsize = self._get_type_maxsize(field, portal_type)
        if type_maxsize is not None:
            return type_maxsize
        if file_size and INamedFileField.providedBy(field):
            return float(file_size)
        elif image_size and INamedImageField.providedBy(field):
            return float(image_size)
        return None

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
            "file_size", interface=ILimitFileSizePanel
        )
        image_size = api.portal.get_registry_record(
            "image_size", interface=ILimitFileSizePanel
        )
        if metatypes[0] == "File" and file_size:
            return float(file_size)
        elif metatypes[0] == "Image" and image_size:
            return float(image_size)
        return 0
