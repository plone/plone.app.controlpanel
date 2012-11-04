from zope.schema.vocabulary import SimpleVocabulary
from plone.app.vocabularies.types import BAD_TYPES
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import adapts
from zope.component import getAdapter
from zope.interface import implements
from plone.app.controlpanel.interfaces import ISearchSchema
from plone.app.controlpanel import _
from Products.CMFCore.utils import getToolByName

anon_auth_items = (('anon', _(u'anonymous users')),
                   ('auth', _(u'logged in users'),))

anon_auth_terms = [SimpleTerm(item[0], title=item[1]) for item in
                   anon_auth_items]

AnonAuthVocabulary = SimpleVocabulary(anon_auth_terms)


class SearchControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(ISearchSchema)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        pprop = getToolByName(context, 'portal_properties')
        self.context = pprop.site_properties
        self.jstool = getToolByName(context, 'portal_javascripts')
        self.ttool = getToolByName(context, 'portal_types')

    def get_enable_livesearch(self):
        return self.context.enable_livesearch

    def set_enable_livesearch(self, value):
        if value:
            self.context.manage_changeProperties(enable_livesearch=True)
            self.jstool.getResource('livesearch.js').setEnabled(True)
        else:
            self.context.manage_changeProperties(enable_livesearch=False)
            self.jstool.getResource('livesearch.js').setEnabled(False)
        self.jstool.cookResources()

    enable_livesearch = property(get_enable_livesearch, set_enable_livesearch)

    def get_types_not_searched(self):
        # Note: we do not show BAD_TYPES.
        return [
            t for t in self.ttool.listContentTypes()
            if t not in self.context.types_not_searched and
            t not in BAD_TYPES
        ]

    def set_types_not_searched(self, value):
        # Note: we add BAD_TYPES to the value list.
        value = [
            t for t in self.ttool.listContentTypes() if t not in value
            or t in BAD_TYPES
        ]
        self.context._updateProperty('types_not_searched', value)

    # This also defines the user friendly types
    types_not_searched = property(
        get_types_not_searched,
        set_types_not_searched
    )


def syncPloneAppRegistryToSearchPortalProperties(settings, event):
    portal = getSite()
    search_properties = getAdapter(portal, ISearchSchema)

    if event.record.fieldName == "enable_livesearch":
        search_properties.enable_livesearch = settings.enable_livesearch
        return
