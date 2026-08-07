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
    label = _("Limit file size settings")
    description = _(
        "help_limit_file_size_panel", default="Set file size for file and image"
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
        # "z3cform-jsonwidget-bundle" was the bundle name before
        # collective.z3cform.jsonwidget's Plone 6 port renamed it to
        # "z3cform-jsonwidget" (see its CHANGES.rst); this call was a
        # no-op ever since, only masked by that bundle being enabled
        # unconditionally. Also request "react-bundle" (from
        # redturtle.reactbundle), which the widget needs and which is
        # similarly gated behind an explicit opt-in.
        add_bundle_on_request(self.request, "react-bundle")
        add_bundle_on_request(self.request, "z3cform-jsonwidget")
        return super().__call__()

    form = LimitFileSizeEditForm
