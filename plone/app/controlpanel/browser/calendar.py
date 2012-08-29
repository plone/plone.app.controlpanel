
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.app.registry.browser import controlpanel

from plone.app.controlpanel import _
from plone.app.controlpanel.interfaces import ICalendarSchema


class CalendarControlPanelForm(controlpanel.RegistryEditForm):

    id = "CalendarControlPanel"
    label = _(u"Calendar settings")
    schema = ICalendarSchema

    def updateFields(self):
        super(CalendarControlPanelForm, self).updateFields()
        self.fields['calendar_states'].widgetFactory = \
            CheckBoxFieldWidget


class CalendarControlPanel(controlpanel.ControlPanelFormWrapper):
    form = CalendarControlPanelForm
