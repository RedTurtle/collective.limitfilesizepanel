# -*- coding: utf-8 -*-

from collective.limitfilesizepanel import messageFactory as _
from plone.registry.field import PersistentField
from z3c.form.object import registerFactoryAdapter
from zope import schema
from zope.interface import Interface
from zope.interface import implements


class ILimitFileSizePanelLayer(Interface):
    """
    Browserlayer
    """


class ICheckSizeUtility(Interface):
    """
    Marker interface for CheckSize utility
    """


class ITypesSettings(Interface):
    """A single unit of size limit for a type and field name"""

    content_type = schema.Choice(
        title=_(u"Content type"),
        vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes',
        required=True)

    field_name = schema.TextLine(
        title=_(u"Field name"),
        description=_(
            'help_field_name',
            default=u"Low level field name, commonly \"image\" or \"file\"."),
        required=True)

    size = schema.Int(
        title=_(u"Size limit"),
        description=_(
            u"Type here a number in MB which will"
            u" limit the field size upload"),
        default=30,
        required=True
    )


class TypesSettings(object):
    implements(ITypesSettings)

    def __init__(self, content_type=None, field_name=None, size=None):
        self.content_type = content_type
        self.field_name = field_name
        self.size = size


class PersistentObject(PersistentField, schema.Object):
    pass


class ILimitFileSizePanel(Interface):
    """
    Settings used in the control panel
    """

    file_size = schema.Int(
        title=_(u"Set the file-type size limit"),
        description=_(
            u"Type here a number in MB which will limit the file size upload"),
        default=30,
    )

    image_size = schema.Int(
        title=_(u"Set the image-type size limit"),
        description=_(
            u"Type here a number in MB which will"
            u" limit the image size upload"),
        default=10,
    )

    types_settings = schema.Tuple(
        title=_(u'Settings for other content types and fields'),
        description=_(
            'help_types_settings',
            default=u"Use this section to provide size overrides of"
                    u" values above.\nProvide a content type/field ID,"
                    u" and the size limit."),
        value_type=PersistentObject(
            ITypesSettings,
            title=_(u"Content/field settings")),
        required=False,
        default=(),
        missing_value=(),
    )

    new_data_only = schema.Bool(
        title=_(u"Validate only new data"),
        description=_(
            "help_new_data_only",
            default=u"Keep selected to validate only new uploaded files and"
                    u" images.\nIf you unselect this and the size "
                    u"configurations above will be lowered, is possible that"
                    u" users that edit contents wont be able to save the form "
                    u"because the validator will check also data already"
                    u" saved."),
        default=True,
    )


registerFactoryAdapter(ITypesSettings, TypesSettings)
