from plone.app.registry.browser import controlpanel

from plone.app.controlpanel import _
from plone.app.controlpanel.interfaces import ISkinsSchema


class SkinsControlPanelForm(controlpanel.RegistryEditForm):

    id = "SkinsControlPanel"
    label = _(u"Skins settings")
    description = _("Settings that affect the site's look and feel.")
    schema = ISkinsSchema

    #form_fields['theme'].custom_widget = DropdownChoiceWidget

    def _on_save(self, data=None):
        # Force a refresh of the page so that a new theme choice fully takes
        # effect.
        if not self.errors and self.adapters['ISkinsSchema'].themeChanged:
            self.request.response.redirect(self.request.URL)


class SkinsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SkinsControlPanelForm
