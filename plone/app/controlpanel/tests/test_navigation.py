# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.registry import Registry
from plone.app.controlpanel.interfaces import INavigationSchema

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class NavigationRegistrySchemaTest(unittest.TestCase):
    """Test that the navigation settings are stored as plone.app.registry
    settings.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.registry = Registry()
        self.registry.registerInterface(INavigationSchema)

    def test_generate_tabs(self):
        self.assertTrue('generate_tabs' in INavigationSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'INavigationSchema.generate_tabs'],
            True)

    def test_nonfolderish_tabs(self):
        self.assertTrue('nonfolderish_tabs' in INavigationSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'INavigationSchema.nonfolderish_tabs'],
            True)

    def test_displayed_types(self):
        self.assertTrue('displayed_types' in INavigationSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'INavigationSchema.displayed_types'],
            ())

    def test_filter_on_workflow(self):
        self.assertTrue('filter_on_workflow' in INavigationSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'INavigationSchema.filter_on_workflow'],
            False)

    def test_workflow_states_to_show(self):
        self.assertTrue('workflow_states_to_show' in INavigationSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'INavigationSchema.workflow_states_to_show'],
            ())

    def test_show_excluded_items(self):
        self.assertTrue('show_excluded_items' in INavigationSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'INavigationSchema.show_excluded_items'],
            True)


class NavigationControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the navigation control panel are actually
    stored in the registry.
    """

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization',
                'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
            )

    def test_navigation_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Navigation').click()
        self.assertTrue("Navigation settings" in self.browser.contents)

    def test_navigation_control_panel_backlink(self):
        self.browser.open(
            "%s/@@navigation-controlpanel" % self.portal_url)
        self.assertTrue("Plone Configuration" in self.browser.contents)

    def test_navigation_control_panel_sidebar(self):
        self.browser.open(
            "%s/@@navigation-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@overview-controlpanel')

    def test_generate_tabs(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INavigationSchema)
        self.browser.open(
            "%s/@@navigation-controlpanel" % self.portal_url)
        self.assertEqual(settings.generate_tabs, True)
        self.assertEqual(
            self.browser.getControl('Automatically generate tabs').selected,
            True
            )
        self.browser.getControl('Automatically generate tabs').selected = False
        self.browser.getControl('Save').click()

        self.assertEqual(settings.generate_tabs, False)


class NavigationControlPanelAdapterFunctionalTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.siteProps = pprop['site_properties']
        self.navProps = pprop['navtree_properties']
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization',
                'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
            )

    def test_generate_tabs(self):
        self.assertEqual(self.siteProps.disable_folder_sections, False)
        self.browser.open(
            "%s/@@navigation-controlpanel" % self.portal_url)
        self.browser.getControl(
            'Automatically generate tabs').selected = False
        self.browser.getControl('Save').click()

        self.assertEqual(self.siteProps.disable_folder_sections, True)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
