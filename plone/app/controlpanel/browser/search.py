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


class SearchControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SearchControlPanelForm
