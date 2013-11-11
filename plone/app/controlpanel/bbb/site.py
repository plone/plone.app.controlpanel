from zope.component import getAdapter

from zope.component import adapts

from zope.interface import implements

from zope.site.hooks import getSite

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode

from plone.app.controlpanel.interfaces import ISiteSchema


class SiteControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(ISiteSchema)

    def __init__(self, context):
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.site_properties
        self.encoding = pprop.site_properties.default_charset

    def get_site_title(self):
        title = getattr(self.portal, 'title', u'')
        return safe_unicode(title)

    def set_site_title(self, value):
        self.portal.title = value.encode(self.encoding)

    def get_site_description(self):
        description = getattr(self.portal, 'description', u'')
        return safe_unicode(description)

    def set_site_description(self, value):
        if value is not None:
            self.portal.description = value.encode(self.encoding)
        else:
            self.portal.description = ''

    def get_webstats_js(self):
        description = getattr(self.context, 'webstats_js', u'')
        return safe_unicode(description)

    def set_webstats_js(self, value):
        if value is not None:
            self.context.webstats_js = value.encode(self.encoding)
        else:
            self.context.webstats_js = u''

    site_title = property(get_site_title, set_site_title)
    site_description = property(get_site_description, set_site_description)
    webstats_js = property(get_webstats_js, set_webstats_js)

    enable_sitemap = ProxyFieldProperty(ISiteSchema['enable_sitemap'])
    exposeDCMetaTags = ProxyFieldProperty(ISiteSchema['exposeDCMetaTags'])
