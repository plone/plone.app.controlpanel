from Products.CMFCore.utils import getToolByName
from zope.site.hooks import getSite
from logging import getLogger
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import ISecuritySchema

log = getLogger('Plone')


class SecurityControlPanel(controlpanel.RegistryEditForm):

    schema = ISecuritySchema
    label = _(u"Security settings")
    description = _(u"""""")

    def updateFields(self):
        super(SecurityControlPanel, self).updateFields()

    def updateWidgets(self):
        super(SecurityControlPanel, self).updateWidgets()

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@security-controlpanel")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Changes canceled."),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


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


class SecurityControlPanelView(controlpanel.ControlPanelFormWrapper):
    form = SecurityControlPanel
