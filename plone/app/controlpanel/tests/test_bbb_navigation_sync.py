import unittest
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.interfaces import INavigationSchema

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class TestSyncPloneAppRegistryToNavigationPortalProperties(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties
        self.nav_properties = ptool.navtree_properties
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(INavigationSchema)

    def test_sync_generate_tabs(self):
        self.assertEquals(self.site_properties.disable_folder_sections, False)
        self.assertEquals(self.settings.generate_tabs, True)
        self.settings.generate_tabs = False
        self.assertEquals(self.site_properties.disable_folder_sections, True)

    def test_sync_nonfolderish_tabs(self):
        self.assertEquals(
            self.site_properties.disable_nonfolderish_sections,
            False)
        self.assertEquals(self.settings.nonfolderish_tabs, True)
        self.settings.nonfolderish_tabs = False
        self.assertEquals(
            self.site_properties.disable_nonfolderish_sections,
            True)

    def test_sync_displayed_types(self):
        self.assertTrue(
            'Discussion Item' in self.nav_properties.metaTypesNotToList)
        self.settings.displayed_types = ('Discussion Item',)
        self.assertTrue(
            'Discussion Item' not in self.nav_properties.metaTypesNotToList)

    def test_sync_filter_on_workflow(self):
        self.assertEquals(self.nav_properties.enable_wf_state_filtering, False)
        self.assertEquals(self.settings.filter_on_workflow, False)
        self.settings.filter_on_workflow = True
        self.assertEquals(self.nav_properties.enable_wf_state_filtering, True)

    def test_sync_workflow_states_to_show(self):
        self.assertEquals(self.nav_properties.wf_states_to_show, ())
        self.assertEquals(self.settings.workflow_states_to_show, ())
        self.settings.workflow_states_to_show = ('private',)
        self.assertEquals(self.nav_properties.wf_states_to_show, ('private',))

    def test_sync_show_excluded_items(self):
        self.assertEquals(self.nav_properties.showAllParents, True)
        self.assertEquals(self.settings.show_excluded_items, True)
        self.settings.show_excluded_items = False
        self.assertEquals(self.nav_properties.showAllParents, False)
