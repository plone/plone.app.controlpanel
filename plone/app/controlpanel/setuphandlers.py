from Products.CMFCore.utils import getToolByName
from plone.app.vocabularies.types import BAD_TYPES
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from plone.app.controlpanel.interfaces import IEditingSchema
from plone.app.controlpanel.interfaces import IMailSchema
from plone.app.controlpanel.interfaces import INavigationSchema
from plone.app.controlpanel.interfaces import ISecuritySchema


def synchronizeRegistrySettingsWithPortalProperties(portal):
    ttool = getToolByName(portal, 'portal_types')
    pprop = getToolByName(portal, 'portal_properties')
    siteProps = pprop['site_properties']
    navProps = pprop['navtree_properties']

    registry = queryUtility(IRegistry)
    settings = registry.forInterface(INavigationSchema)
    settings.generate_tabs = not siteProps.disable_folder_sections
    settings.nonfolderish_tabs = not siteProps.disable_nonfolderish_sections

    allTypes = ttool.listContentTypes()
    displayed_types = tuple([
        t for t in allTypes \
        if t not in navProps.metaTypesNotToList])
    settings.displayed_types = displayed_types

    settings.filter_on_workflow = navProps.enable_wf_state_filtering
    settings.workflow_states_to_show = navProps.wf_states_to_show


def setupVarious(context):
    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('plone.app.controlpanel.marker.txt') is None:
        # Not your add-on
        return

    portal = context.getSite()

    synchronizeRegistrySettingsWithPortalProperties(portal)
