# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage
from collective.limitfilesizepanel import messageFactory as _
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from plone.app.registry.browser import controlpanel
from z3c.form import button


class LimitFileSizeEditForm(controlpanel.RegistryEditForm):
    """Media settings form.
    """
    schema = ILimitFileSizePanel
    id = "LimitFileSizeEditForm"
    label = _(u"Limit file size settings")
    description = _(u"help_limit_file_size_panel",
                    default=u"Set file size for file and image")

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@limitfilesize-settings")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))

    def updateWidgets(self):
        super(LimitFileSizeEditForm, self).updateWidgets()
        self.widgets['file_size'].maxlength = 5
        self.widgets['file_size'].size = 5
        self.widgets['image_size'].maxlength = 5
        self.widgets['image_size'].size = 5
        for widget in self.widgets['types_settings'].widgets:
            widget.subform.widgets['size'].maxlength = 5
            widget.subform.widgets['size'].size = 5


class LimitFileSizeControlPanel(controlpanel.ControlPanelFormWrapper):
    """Analytics settings control panel.
    """
    form = LimitFileSizeEditForm
