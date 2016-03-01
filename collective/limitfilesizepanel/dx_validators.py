# -*- coding: utf-8 -*-
from plone.namedfile.interfaces import INamedBlobImageField
from plone.namedfile.interfaces import INamedBlobFileField
# from plone.app.contenttypes.interfaces import IImage
from zope.interface import Invalid
from z3c.form import validator
from plone import api
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel


# 1 MB size limit
MAXSIZE = 1024 * 1024


class DXFileSizeValidator(validator.FileUploadValidator):

    def get_max_size(self):
        types_settings_list = api.portal.get_registry_record(
            'types_settings',
            interface=ILimitFileSizePanel)
        # first of all, check if the current context has a specific limit for
        # the current field
        for type_settings in types_settings_list:
            if self.view.portal_type == type_settings.content_type and \
               self.field.getName() == type_settings.field_name:
                return float(type_settings.size)
        # if not, use default limits
        if INamedBlobImageField.providedBy(self.field):
            return float(api.portal.get_registry_record(
                'image_size',
                interface=ILimitFileSizePanel))
        elif INamedBlobFileField.providedBy(self.field):
            return float(api.portal.get_registry_record(
                'file_size',
                interface=ILimitFileSizePanel))
        return 0

    def validate(self, value):
        import logging
        logger=logging.getLogger("limitfilesizepanel")
        logger.info("QUI!!!!")

        super(DXFileSizeValidator, self).validate(value)
        if not value:
            return
        new_data_only = api.portal.get_registry_record(
            'new_data_only',
            interface=ILimitFileSizePanel)
        if new_data_only and \
           self.view.portal_type == self.view.context.portal_type:
            # we are in edit and we don't want to check sizes..skip
            return
        max_size = self.get_max_size()
        if not max_size:
            return
        size = float(value.getSize())
        sizeMB = (size / (1024 * 1024))
        if sizeMB > max_size:
            raise Invalid(
                "The file is too large (%.2fmb). Maximum size is %smb"
                % (sizeMB, max_size))


validator.WidgetValidatorDiscriminators(DXFileSizeValidator,
                                        field=INamedBlobImageField)

validator.WidgetValidatorDiscriminators(DXFileSizeValidator,
                                        field=INamedBlobFileField)
