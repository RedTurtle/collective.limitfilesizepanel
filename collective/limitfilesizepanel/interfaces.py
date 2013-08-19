# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema
from collective.limitfilesizepanel import messageFactory as _


class ILimitFileSizePanel(Interface):
    """
    Settings used in the control panel
    """

    file_size = schema.Int(
        title=_(u"Set the file-type size limit"),
        description=_(u"Type here a number in MB which will limit the file size upload"),
        default=30,
    )

    image_size = schema.Int(
        title=_(u"Set the image-type size limit"),
        description=_(u"Type here a number in MB which will limit the image size upload"),
        default=10,
    )

    new_data_only = schema.Bool(
        title=_(u"Validate only new data"),
        description=_("help_new_data_only",
                      default=u"Keep selected to validate only new uploaded files and images.\n"
                              u"If you unselect this and the size configurations above will be lowered, "
                              u"is possible that users that edit contents wont be able to save the form "
                              u"because the validator will check also data already saved."),
        default=True,
    )
