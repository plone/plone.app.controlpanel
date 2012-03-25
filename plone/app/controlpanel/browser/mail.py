from zope.component import getUtility
from Products.CMFPlone.utils import safe_hasattr
from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from zope.component import adapts
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from zope.interface import implements
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import IMailSchema


class MailSettingsControlPanel(controlpanel.RegistryEditForm):

    schema = IMailSchema
    label = _(u"Mail settings")
    description = _(u"""""")

    def updateFields(self):
        super(MailSettingsControlPanel, self).updateFields()

    def updateWidgets(self):
        super(MailSettingsControlPanel, self).updateWidgets()

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@mail-controlpanel")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Changes canceled."),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


def updateMailSettings(settings, event):
    portal = getSite()
    mailhost = getToolByName(portal, 'MailHost')
    mailhost.smtp_host = settings.smtp_host
    mailhost.smtp_port = settings.smtp_port
    mailhost.smtp_userid = settings.smtp_userid
    mailhost.smtp_pass = settings.smtp_pass
    getUtility(ISiteRoot).email_from_name = \
        settings.email_from_name
    getUtility(ISiteRoot).email_from_address = settings.email_from_address


class MailControlPanel(controlpanel.ControlPanelFormWrapper):
    form = MailSettingsControlPanel
