from zope.interface import Interface
from zope.component import adapts
from zope.formlib.form import FormFields
from zope.interface import implements
from zope.schema import TextLine

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode

from plone.app.controlpanel.form import ControlPanelForm

class IProxySchema(Interface):
    http_proxy = TextLine(title=_(u'HTTP proxy'),
                          description=_(u"This is the URL for the HTTP "
                                        "proxy that will be used when "
                                        "retrieving syndication feeds, "
                                        "etc."),
                          default=u'',
                          required=False)

    ftp_proxy = TextLine(title=_(u'FTP proxy'),
                         description=_(u"This is the URL for the FTP "
                                        "proxy that will be used when "
                                        "Plone is retrieving files, "
                                        "etc."),
                         default=u'',
                         required=False)


class ProxyControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IProxySchema)

    def __init__(self, context):
        self.portal = context
        super(ProxyControlPanelAdapter, self).__init__(context)
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.site_properties
        self.encoding = pprop.site_properties.default_charset

    def get_http_proxy(self):
        return self.context.getProperty('http_proxy', None)

    def set_http_proxy(self, value):
        if value:
            if not self.context.hasProperty('http_proxy'):
                self.context.manage_addProperty('http_proxy', '', 'string')
            self.context.http_proxy = value.encode(self.encoding)
        else:
            if self.context.hasProperty('http_proxy'):
                self.context._delProperty('http_proxy')

    def get_ftp_proxy(self):
        return self.context.getProperty('ftp_proxy', None)

    def set_ftp_proxy(self, value):
        if value:
            if not self.context.hasProperty('ftp_proxy'):
                self.context.manage_addProperty('ftp_proxy', '', 'string')
            self.context.ftp_proxy = value.encode(self.encoding)
        else:
            if self.context.hasProperty('ftp_proxy'):
                self.context._delProperty('ftp_proxy')

    http_proxy = property(get_http_proxy, set_http_proxy)
    ftp_proxy = property(get_ftp_proxy, set_ftp_proxy)


class ProxyControlPanel(ControlPanelForm):

    form_fields = FormFields(IProxySchema)

    label = _("Proxy settings")
    description = _("Proxy settings to enable the Plone server to access other servers through a proxy.")
    form_name = _("Proxy settings")
