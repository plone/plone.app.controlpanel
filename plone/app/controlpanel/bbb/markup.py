from zope.site.hooks import getSite
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import adapts
from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.interfaces import IMarkupSchema

from Products.Archetypes.mimetype_utils import getDefaultContentType, \
    setDefaultContentType, getAllowedContentTypes, getAllowableContentTypes, \
    setForbiddenContentTypes


class MarkupControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(IMarkupSchema)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.pmembership = getToolByName(context, 'portal_membership')
        portal_url = getToolByName(context, 'portal_url')
        self.portal = portal_url.getPortalObject()
        self.context = pprop.site_properties

    def get_default_type(self):
        return getDefaultContentType(self.context)

    def set_default_type(self, value):
        setDefaultContentType(self.context, value)

    default_type = property(get_default_type, set_default_type)

    def get_allowed_types(self):
        return getAllowedContentTypes(self.context)

    def set_allowed_types(self, value):
        # The menu pretends to be a whitelist, but we are storing a blacklist
        # so that new types are available by default. So, we inverse the list.
        allowable_types = getAllowableContentTypes(self.context)
        forbidden_types = [t for t in allowable_types if t not in value]
        setForbiddenContentTypes(self.context, forbidden_types)

    allowed_types = property(get_allowed_types, set_allowed_types)
