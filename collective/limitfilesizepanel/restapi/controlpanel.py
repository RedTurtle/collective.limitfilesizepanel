from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanelControlpanel
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanelLayer
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@adapter(Interface, ILimitFileSizePanelLayer)
@implementer(ILimitFileSizePanelControlpanel)
class LimitFileSizeControlpanel(RegistryConfigletPanel):
    schema = ILimitFileSizePanel
    configlet_id = "limitfilesize-settings"
    configlet_category_id = "Products"
    schema_prefix = None
