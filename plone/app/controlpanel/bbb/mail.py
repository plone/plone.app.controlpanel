from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from Products.CMFCore.interfaces import ISiteRoot
from zope.site.hooks import getSite
from Products.CMFPlone.utils import safe_hasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.interfaces import IMailSchema


class MailControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(IMailSchema)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.encoding = pprop.site_properties.default_charset
        self.context = getToolByName(self.portal, 'MailHost')

    def get_smtp_host(self):
        return getattr(self.context, 'smtp_host', None)

    def set_smtp_host(self, value):
        if safe_hasattr(self.context, 'smtp_host'):
            self.context.smtp_host = value

    smtp_host = property(get_smtp_host, set_smtp_host)

    def get_smtp_port(self):
        return getattr(self.context, 'smtp_port', None)

    def set_smtp_port(self, value):
        if safe_hasattr(self.context, 'smtp_port'):
            self.context.smtp_port = value

    smtp_port = property(get_smtp_port, set_smtp_port)

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


def syncPloneAppRegistryToMailhostProperties(settings, event):
    portal = getSite()
    mailhost = getToolByName(portal, 'MailHost')

    if event.record.fieldName == "smtp_host":
        mailhost.smtp_host = settings.smtp_host
        return

    if event.record.fieldName == "smtp_port":
        mailhost.smtp_port = settings.smtp_port
        return

    if event.record.fieldName == "smtp_userid":
        mailhost.smtp_uid = settings.smtp_userid
        return

    if event.record.fieldName == "smtp_pass":
        mailhost.smtp_pwd = settings.smtp_pass
        return

    if event.record.fieldName == "email_from_name":
        getUtility(ISiteRoot).email_from_name = \
            settings.email_from_name
        return

    if event.record.fieldName == "email_from_address":
        getUtility(ISiteRoot).email_from_address = settings.email_from_address
        return
