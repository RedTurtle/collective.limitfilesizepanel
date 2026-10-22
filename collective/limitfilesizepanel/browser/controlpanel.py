from collective.limitfilesizepanel import messageFactory as _
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from plone.app.registry.browser import controlpanel
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

    def updateWidgets(self):
        super().updateWidgets()
        self.widgets["file_size"].maxlength = 5
        self.widgets["file_size"].size = 5
        self.widgets["image_size"].maxlength = 5
        self.widgets["image_size"].size = 5


class LimitFileSizeControlPanel(controlpanel.ControlPanelFormWrapper):
    """Analytics settings control panel."""

    form = LimitFileSizeEditForm
