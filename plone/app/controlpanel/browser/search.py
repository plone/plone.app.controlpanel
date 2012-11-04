from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import ISearchSchema


class SearchControlPanelForm(controlpanel.RegistryEditForm):

    id = "SearchControlPanel"
    label = _(u"Search settings")
    schema = ISearchSchema

    #form_fields = FormFieldsets(searchset)
    #form_fields['types_not_searched'].custom_widget = MCBThreeColumnWidget
    #form_fields['types_not_searched'].custom_widget.cssClass='label'

    def updateFields(self):
        super(SearchControlPanelForm, self).updateFields()
        self.fields['types_not_searched'].widgetFactory = \
            CheckBoxFieldWidget


class SearchControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SearchControlPanelForm
