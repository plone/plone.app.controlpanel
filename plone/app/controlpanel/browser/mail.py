from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from zope.component import adapts
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from zope.interface import implements
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope import schema
from zope.interface import Interface

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel


class IMailSchema(Interface):
    """Combined schema for the adapter lookup.
    """

    smtp_host = schema.TextLine(
        title=_(u'label_smtp_server',
                default=u'SMTP server'),
        description=_(u"help_smtp_server",
                     default=u"The address of your local "
                     "SMTP (outgoing e-mail) server. Usually "
                     "'localhost', unless you use an "
                     "external server to send e-mail."),
        default=u'localhost',
        required=True)

    smtp_port = schema.Int(
        title=_(u'label_smtp_port',
                default=u'SMTP port'),
        description=_(u"help_smtp_port",
                      default=u"The port of your local SMTP "
                      "(outgoing e-mail) server. Usually '25'."),
        default=25,
        required=True)

    smtp_userid = schema.TextLine(
        title=_(u'label_smtp_userid',
               default=u'ESMTP username'),
        description=_(u"help_smtp_userid",
                     default=u"Username for authentication "
                     "to your e-mail server. Not required "
                     "unless you are using ESMTP."),
        default=None,
        required=False)

    smtp_pass = schema.Password(
        title=_(u'label_smtp_pass',
               default=u'ESMTP password'),
        description=_(u"help_smtp_pass",
                     default=u"The password for the ESMTP "
                     "user account."),
        default=None,
        required=False)

    email_from_name = schema.TextLine(
        title=_(u"Site 'From' name"),
        description=_(u"Plone generates e-mail using "
                      "this name as the e-mail "
                      "sender."),
        default=None,
        required=True)

    email_from_address = schema.ASCII(
        title=_(u"Site 'From' address"),
        description=_(u"Plone generates e-mail using "
                      "this address as the e-mail "
                      "return address. It is also "
                      "used as the destination "
                      "address for the site-wide "
                      "contact form and the 'Send test "
                      "e-mail' feature."),
        default=None,
        required=True)


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

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.utils import safe_hasattr


class MailControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(IMailSchema)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.encoding = pprop.site_properties.default_charset
        self.context = getToolByName(self.portal, 'MailHost')

    smtp_host = ProxyFieldProperty(IMailSchema['smtp_host'])
    smtp_port = ProxyFieldProperty(IMailSchema['smtp_port'])

    def get_smtp_userid(self):
        return getattr(self.context, 'smtp_userid',
                       getattr(self.context, 'smtp_uid', None))

    def set_smtp_userid(self, value):
        if safe_hasattr(self.context, 'smtp_userid'):
            self.context.smtp_userid = value
            #SecureMailhost 1.x also uses this:
            if safe_hasattr(self.context, '_smtp_userid'):
                self.context._smtp_userid = value
        elif safe_hasattr(self.context, 'smtp_uid'):
            self.context.smtp_uid = value

    smtp_userid = property(get_smtp_userid, set_smtp_userid)

    def get_smtp_pass(self):
        return getattr(self.context, 'smtp_pass',
                       getattr(self.context, 'smtp_pwd', None))

    def set_smtp_pass(self, value):
        # Don't update the value, if we don't get a new one
        if value is not None:
            if safe_hasattr(self.context, 'smtp_pass'):
                self.context.smtp_pass = value
                #SecureMailhost 1.x also uses this:
                if safe_hasattr(self.context, '_smtp_pass'):
                    self.context._smtp_pass = value
            elif safe_hasattr(self.context, 'smtp_pwd'):
                self.context.smtp_pwd = value

    smtp_pass = property(get_smtp_pass, set_smtp_pass)

    def get_email_from_name(self):
        return getUtility(ISiteRoot).email_from_name

    def set_email_from_name(self, value):
        getUtility(ISiteRoot).email_from_name = value

    email_from_name = property(get_email_from_name, set_email_from_name)

    def get_email_from_address(self):
        return getUtility(ISiteRoot).email_from_address

    def set_email_from_address(self, value):
        getUtility(ISiteRoot).email_from_address = value

    email_from_address = property(get_email_from_address,
                                  set_email_from_address)
