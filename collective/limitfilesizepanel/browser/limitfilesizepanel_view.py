from Acquisition import aq_base
from collective.limitfilesizepanel import messageFactory as _
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from plone import api
from plone.api.exc import InvalidParameterError
from plone.namedfile.interfaces import INamedFileField
from plone.namedfile.interfaces import INamedImageField
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Interface
from ZPublisher.HTTPRequest import FileUpload


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
                default="Validation failed. Uploaded data is too large:"
                " ${size}MB (max ${max}MB)",
                mapping={
                    "size": safe_unicode(f"{sizeMB:.1f}"),
                    "max": safe_unicode(f"{maxsize:.1f}"),
                },
            )
            result["error"] = translate(msg, context=self.request)
        return result

    def canBypassValidation(self):
        """Check if the user has bypass permission"""

        return api.user.has_permission(
            "collective.limitfilesizepanel: Bypass limit size", obj=self.context
        )

    def get_maxsize(self, field):
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
