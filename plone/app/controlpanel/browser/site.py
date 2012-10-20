from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import ISiteSchema


class SiteControlPanelForm(controlpanel.RegistryEditForm):

    id = "SiteControlPanel"
    label = _(u"Site settings")
    description = _("Site-wide settings.")
    schema = ISiteSchema


class SiteControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SiteControlPanelForm
