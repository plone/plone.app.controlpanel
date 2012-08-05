import unittest
from plone.app.testing import setRoles
from plone.app.controlpanel.browser.navigation import INavigationSchema
from zope.component import getAdapter
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class NavigationControlPanelAdapterTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.ttool = getToolByName(self.portal, 'portal_types')
        pprop = getToolByName(self.portal, 'portal_properties')
        self.siteProps = pprop.site_properties
        self.navProps = pprop.navtree_properties

    def test_adapter_lookup(self):
        self.assertTrue(getAdapter(self.portal, INavigationSchema))

    def test_get_generate_tabs(self):
        self.assertEqual(self.siteProps.disable_folder_sections, False)
        self.siteProps.disable_folder_sections = True
        navigation_settings = getAdapter(self.portal, INavigationSchema)
        self.assertEquals(navigation_settings.generate_tabs, False)

    def test_set_generate_tabs(self):
        navigation_settings = getAdapter(self.portal, INavigationSchema)
        self.assertEqual(navigation_settings.generate_tabs, True)
        navigation_settings.generate_tabs = False
        self.assertEquals(self.siteProps.disable_folder_sections, True)

    def test_get_nonfolderish_tabs(self):
        self.assertEqual(self.siteProps.disable_nonfolderish_sections, False)
        self.siteProps.disable_nonfolderish_sections = True
        navigation_settings = getAdapter(self.portal, INavigationSchema)
        self.assertEquals(navigation_settings.nonfolderish_tabs, False)

    def test_set_nonfolderish_tabs(self):
        pass

    def test_get_show_excluded_items(self):
        self.assertEqual(self.navProps.showAllParents, True)
        self.navProps.show_excluded_items = False
        navigation_settings = getAdapter(self.portal, INavigationSchema)
        self.assertEquals(navigation_settings.show_excluded_items, True)

    def test_set_show_excluded_items(self):
        pass

    def test_get_displayed_types(self):
        self.assertEqual(self.siteProps.disable_nonfolderish_sections, False)
        self.siteProps.disable_nonfolderish_sections = True
        navigation_settings = getAdapter(self.portal, INavigationSchema)
        self.assertEquals(navigation_settings.nonfolderish_tabs, False)

    def test_set_displayed_types(self):
        pass

    def test_get_filter_on_workflow(self):
        pass

    def test_set_filter_on_workflow(self):
        pass

    def test_get_workflow_states_to_show(self):
        pass

    def test_set_workflow_states_to_show(self):
        pass
