from plone.app.registry.browser import controlpanel

from plone.app.controlpanel import _
from plone.app.controlpanel.interfaces import IEditingSchema


class EditingControlPanelForm(controlpanel.RegistryEditForm):

    id = "EditingControlPanel"
    label = _(u"Editing settings")
    schema = IEditingSchema


class EditingControlPanel(controlpanel.ControlPanelFormWrapper):
    form = EditingControlPanelForm
