from zope.site.hooks import getSite

from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import ISecuritySchema


class SecurityControlPanelForm(controlpanel.RegistryEditForm):

    id = "SecurityControlPanel"
    label = _(u"Security settings")
    schema = ISecuritySchema


class SecurityControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SecurityControlPanelForm
