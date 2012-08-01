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
        description=_(u"Type here a number in Mb which will limit the file size upload"),
        default=30,
    )

    image_size = schema.Int(
        title=_(u"Set the image-type size limit"),
        description=_(u"Type here a number in Mb which will limit the image size upload"),
        default=10,
    )
