from zope.component import adapts
from plone.app.controlpanel.browser.mail import IMailSchema
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from zope.component import getUtility
from zope.interface import implements
from Products.CMFCore.interfaces import ISiteRoot
from zope.site.hooks import getSite
from Products.CMFPlone.utils import safe_hasattr
from plone.app.controlpanel.browser.editing import IEditingSchema
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot


class EditingControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(IEditingSchema)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.site_properties
        self.encoding = pprop.site_properties.default_charset

    visible_ids = ProxyFieldProperty(IEditingSchema['visible_ids'])
    enable_inline_editing = ProxyFieldProperty(
        IEditingSchema['enable_inline_editing'])
    enable_link_integrity_checks = ProxyFieldProperty(
        IEditingSchema['enable_link_integrity_checks'])
    ext_editor = ProxyFieldProperty(
        IEditingSchema['ext_editor'])
    default_editor = ProxyFieldProperty(
        IEditingSchema['default_editor'])
    lock_on_ttw_edit = ProxyFieldProperty(
        IEditingSchema['lock_on_ttw_edit'])


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
