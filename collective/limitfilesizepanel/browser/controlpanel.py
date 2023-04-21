# -*- coding: utf-8 -*-
from collective.limitfilesizepanel import messageFactory as _
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.interfaces import ITypesSettingsRow
from collective.z3cform.jsonwidget.browser.widget import JSONFieldWidget
from plone.app.registry.browser import controlpanel
from Products.CMFPlone.resources import add_bundle_on_request
from z3c.form import field


class LimitFileSizeEditForm(controlpanel.RegistryEditForm):
    """Media settings form."""

    schema = ILimitFileSizePanel
    id = "LimitFileSizeEditForm"
    label = _(u"Limit file size settings")
    description = _(
        u"help_limit_file_size_panel", default=u"Set file size for file and image"
    )
    fields = field.Fields(ILimitFileSizePanel)
    fields["types_settings"].widgetFactory = JSONFieldWidget

    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["file_size"].maxlength = 5
        self.widgets["file_size"].size = 5
        self.widgets["image_size"].maxlength = 5
        self.widgets["image_size"].size = 5
        self.widgets["types_settings"].schema = ITypesSettingsRow


class LimitFileSizeControlPanel(controlpanel.ControlPanelFormWrapper):
    """Analytics settings control panel."""

    def __call__(self):
        add_bundle_on_request(self.request, "z3cform-jsonwidget-bundle")
        return super().__call__()

    form = LimitFileSizeEditForm
