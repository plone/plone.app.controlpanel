# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.registry import Registry
from plone.app.controlpanel.interfaces import ISearchSchema

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class SearchRegistryIntegrationTest(unittest.TestCase):
    """Test that the search settings are stored as plone.app.registry
    settings.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.registry = Registry()
        self.registry.registerInterface(ISearchSchema)

    def test_search_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="search-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_plone_app_registry_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            'plone.app.registry' in [a.getAction(self)['id']
            for a in self.controlpanel.listActions()]
        )

    def test_enable_livesearch_setting(self):
        self.assertTrue('enable_livesearch' in ISearchSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISearchSchema.enable_livesearch'],
            False)

    def test_types_not_searched(self):
        self.assertTrue('types_not_searched' in ISearchSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISearchSchema.types_not_searched'],
            (
                'Collection',
                'Document',
                'Event',
                'File',
                'Folder',
                'Link',
                'News Item',
            )
        )


class SearchControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the search control panel are actually
    stored in the registry.
    """

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_search_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Search').click()

    def test_search_control_panel_backlink(self):
        self.browser.open(
            "%s/@@search-controlpanel" % self.portal_url)
        self.assertTrue("Plone Configuration" in self.browser.contents)

    def test_search_control_panel_sidebar(self):
        self.browser.open(
            "%s/@@search-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@overview-controlpanel')

    def test_enable_livesearch(self):
        self.browser.open(
            "%s/@@search-controlpanel" % self.portal_url)
        self.browser.getControl('Enable LiveSearch').selected = True
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISearchSchema)
        self.assertEqual(settings.enable_livesearch, True)


class SearchRegistryIntegrationTest(unittest.TestCase):
    """Test that changes in the search registry are actually applied.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISearchSchema)
        self.site_properties = self.portal.portal_properties.site_properties
        self.mtool = getToolByName(self.portal, "portal_membership")

    def test_enable_livesearch(self):
        self.assertEqual(self.settings.enable_livesearch, True)
        self.assertEqual(self.site_properties.enable_livesearch, True)

        self.settings.enable_livesearch = False

        self.assertEqual(self.settings.enable_livesearch, False)
        self.assertEqual(self.site_properties.enable_livesearch, False)

    def test_types_not_searched(self):
        default_types_not_searched = ('ATBooleanCriterion', 'ATDateCriteria', 'ATDateRangeCriterion', 'ATListCriterion', 'ATPortalTypeCriterion', 'ATReferenceCriterion', 'ATSelectionCriterion', 'ATSimpleIntCriterion', 'ATSimpleStringCriterion', 'ATSortCriterion', 'ChangeSet', 'Discussion Item', 'Plone Site', 'TempFolder', 'ATCurrentAuthorCriterion', 'ATPathCriterion', 'ATRelativePathCriterion')
        self.assertEqual(
            self.settings.types_not_searched,
            default_types_not_searched,
        )
        self.assertEqual(
            self.site_properties.types_not_searched,
            default_types_not_searched,
        )

        self.settings.types_not_searched = ('Event',)

        self.assertEqual(self.settings.types_not_searched, ('Event',))
        self.assertEqual(self.site_properties.types_not_searched, ('Event',))


class SearchControlPanelAdapterFunctionalTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.site_properties = pprop.site_properties
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_enable_livesearch(self):
        self.assertEqual(self.site_properties.enable_livesearch, True)
        self.browser.open(
            "%s/@@search-controlpanel" % self.portal_url)
        self.browser.getControl(
            'Enable LiveSearch').selected = False
        self.browser.getControl('Save').click()

        self.assertEqual(self.site_properties.enable_livesearch, False)

    def test_types_not_searched(self):
        self.assertTrue('Event' not in self.site_properties.types_not_searched)
        self.browser.open(
            "%s/@@search-controlpanel" % self.portal_url)
        self.browser.getControl(name='form.widgets.types_not_searched:list')\
            .value = ['Event']
        self.browser.getControl('Save').click()

        self.assertTrue('Event' in self.site_properties.types_not_searched)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
