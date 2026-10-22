from collective.limitfilesizepanel import messageFactory as _
from plone.restapi.controlpanels import IControlpanel
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

    new_data_only = schema.Bool(
        title=_("Validate only new data"),
        description=_(
            "help_new_data_only",
            default="Keep selected to validate only new uploaded files and"
            " images.\nIf you unselect this and the size "
            "configurations above will be lowered, is possible that"
            " users that edit contents won't be able to save the form "
            "because the validator will check also data already"
            " saved.",
        ),
        default=True,
        # a required Bool can't be unchecked: z3c.form and Volto treat False
        # as a missing value
        required=False,
    )


class ILimitFileSizePanelControlpanel(IControlpanel):
    """
    Control panel exposed on plone.restapi (@controlpanels)
    """
