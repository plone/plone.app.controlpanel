from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel import _
from plone.app.controlpanel.interfaces import IMarkupSchema


class MarkupControlPanelForm(controlpanel.RegistryEditForm):

    id = "MarkupControlPanel"
    label = _(u"Markup settings")
    schema = IMarkupSchema

    def updateFields(self):
        super(MarkupControlPanelForm, self).updateFields()
        self.fields['allowed_types'].widgetFactory = \
            CheckBoxFieldWidget


class MarkupControlPanel(controlpanel.ControlPanelFormWrapper):
    form = MarkupControlPanelForm
