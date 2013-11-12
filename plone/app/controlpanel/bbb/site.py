from zope.component import getAdapter
from zope.component import adapts
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.controlpanel.interfaces import ISiteSchema

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
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISiteSchema)

    def get_site_title(self):
        return self.settings.site_title

    def set_site_title(self, value):
        if isinstance(value, str):
            value = value.decode('utf-8')
        self.settings.site_title = value

    def get_webstats_js(self):
        return self.settings.webstats_js

    def set_webstats_js(self, value):
        if isinstance(value, str):
            value = value.decode('utf-8')
        self.settings.webstats_js = value

    site_title = property(get_site_title, set_site_title)
    webstats_js = property(get_webstats_js, set_webstats_js)

    enable_sitemap = ProxyFieldProperty(ISiteSchema['enable_sitemap'])
    exposeDCMetaTags = ProxyFieldProperty(ISiteSchema['exposeDCMetaTags'])
