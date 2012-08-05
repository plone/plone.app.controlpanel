from Products.CMFCore.utils import getToolByName
from zope.site.hooks import getSite
from logging import getLogger
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import ISecuritySchema

log = getLogger('Plone')


class SecurityControlPanelForm(controlpanel.RegistryEditForm):

    id = "SecurityControlPanel"
    label = _(u"Security settings")
    schema = ISecuritySchema


class SecurityControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SecurityControlPanelForm


def updateSecuritySettings(settings, event):
    """Update Plone's security settings when the security settings in the
    security control panel changes.
    """
    portal = getSite()
    portal.validate_email = not settings.enable_user_pwd_choice
    portal_properties = getToolByName(portal, "portal_properties")
    site_properties = portal_properties.site_properties
    site_properties.allowAnonymousViewAbout = settings.allow_anon_views_about
    site_properties.use_email_as_login = settings.use_email_as_login
    mtool = getToolByName(portal, "portal_membership")
    mtool.memberareaCreationFlag = settings.enable_user_folders
