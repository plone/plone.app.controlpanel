from zope.site.hooks import getSite
from zope.component import adapts
from plone.app.controlpanel.interfaces import INavigationSchema
from zope.interface import implements
from plone.app.vocabularies.types import BAD_TYPES
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot


class NavigationControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(INavigationSchema)

    def __init__(self, context):
        self.context = context
        pprop = getToolByName(context, 'portal_properties')
        self.siteProps = pprop.site_properties
        self.navProps = pprop.navtree_properties
        self.ttool = getToolByName(context, 'portal_types')

    def get_generate_tabs(self):
        return not self.siteProps.getProperty('disable_folder_sections')

    def set_generate_tabs(self, value):
        self.siteProps._updateProperty('disable_folder_sections', not value)

    generate_tabs = property(get_generate_tabs, set_generate_tabs)

    def get_nonfolderish_tabs(self):
        return not self.siteProps.getProperty('disable_nonfolderish_sections')

    def set_nonfolderish_tabs(self, value):
        self.siteProps._updateProperty(
            'disable_nonfolderish_sections', not value)

    nonfolderish_tabs = property(get_nonfolderish_tabs, set_nonfolderish_tabs)

    def get_show_excluded_items(self):
        return self.navProps.getProperty('showAllParents')

    def set_show_excluded_items(self, value):
        self.navProps._updateProperty('showAllParents', value)

    show_excluded_items = property(
        get_show_excluded_items,
        set_show_excluded_items)

    def get_displayed_types(self):
        allTypes = self.ttool.listContentTypes()
        blacklist = self.navProps.metaTypesNotToList
        return [t for t in allTypes if t not in blacklist
                                    and t not in BAD_TYPES]

    def set_displayed_types(self, value):
        # The menu pretends to be a whitelist, but we are storing a blacklist
        # so that new types are searchable by default. Inverse the list.
        allTypes = self.ttool.listContentTypes()
        blacklistedTypes = [t for t in allTypes if t not in value
                                                or t in BAD_TYPES]
        self.navProps._updateProperty('metaTypesNotToList', blacklistedTypes)

    displayed_types = property(get_displayed_types, set_displayed_types)

    def get_filter_on_workflow(self):
        return self.navProps.getProperty('enable_wf_state_filtering')

    def set_filter_on_workflow(self, value):
        self.navProps._updateProperty('enable_wf_state_filtering', value)

    filter_on_workflow = property(
        get_filter_on_workflow,
        set_filter_on_workflow)

    def get_workflow_states_to_show(self):
        return self.navProps.getProperty('wf_states_to_show')

    def set_workflow_states_to_show(self, value):
        self.navProps._updateProperty('wf_states_to_show', value)

    workflow_states_to_show = property(
        get_workflow_states_to_show,
        set_workflow_states_to_show)
