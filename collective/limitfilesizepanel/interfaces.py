# -*- coding: utf-8 -*-
from collective.limitfilesizepanel import messageFactory as _
from zope import schema
from zope.interface import Interface


class ILimitFileSizePanelLayer(Interface):
    """
    Browserlayer
    """


class ICheckSizeUtility(Interface):
    """
    Marker interface for CheckSize utility
    """


class ITypesSettingsRow(Interface):
    """A single unit of size limit for a type and field name"""

    content_type = schema.Choice(
        title=_("Content type"),
        vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes",
        required=True,
    )

    field_name = schema.TextLine(
        title=_("Field name"),
        description=_(
            "help_field_name",
            default='Low level field name, commonly "image" or "file".',
        ),
        required=True,
    )

    size = schema.Int(
        title=_("Size limit"),
        description=_(
            "Type here a number in MB which will" " limit the field size upload"
        ),
        default=30,
        required=True,
    )


class ILimitFileSizePanel(Interface):
    """
    Settings used in the control panel
    """

    file_size = schema.Int(
        title=_("Set the file-type size limit"),
        description=_("Type here a number in MB which will limit the file size upload"),
        default=30,
    )

    image_size = schema.Int(
        title=_("Set the image-type size limit"),
        description=_(
            "Type here a number in MB which will" " limit the image size upload"
        ),
        default=10,
    )

    types_settings = schema.SourceText(
        title=_("Settings for other content types and fields"),
        description=_(
            "help_types_settings",
            default="Use this section to provide size overrides of"
            " values above.\nProvide a content type/field ID,"
            " and the size limit.",
        ),
        required=False,
    )

    new_data_only = schema.Bool(
        title=_("Validate only new data"),
        description=_(
            "help_new_data_only",
            default="Keep selected to validate only new uploaded files and"
            " images.\nIf you unselect this and the size "
            "configurations above will be lowered, is possible that"
            " users that edit contents wont be able to save the form "
            "because the validator will check also data already"
            " saved.",
        ),
        default=True,
    )
