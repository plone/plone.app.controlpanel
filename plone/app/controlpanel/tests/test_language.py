# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.registry import Registry
from plone.app.controlpanel.interfaces import ILanguageSchema

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class LanguageRegistryIntegrationTest(unittest.TestCase):
    """Test that the language settings are stored as plone.app.registry
    settings.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.registry = Registry()
        self.registry.registerInterface(ILanguageSchema)

    def test_language_controlpanel_view(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST),
            name="language-controlpanel"
        )
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_plone_app_registry_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            'plone.app.registry' in [a.getAction(self)['id']
            for a in self.controlpanel.listActions()]
        )

    def test_use_combined_language_codes_setting(self):
        self.assertTrue(
            'use_combined_language_codes' in ILanguageSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ILanguageSchema.use_combined_language_codes'],
            False)

    def test_default_language_setting(self):
        self.assertTrue('default_language' in ILanguageSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ILanguageSchema.default_language'],
            False)


class LanguageControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the language control panel are actually
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

    def test_language_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Language').click()

    def test_language_control_panel_backlink(self):
        self.browser.open(
            "%s/@@language-controlpanel" % self.portal_url)
        self.assertTrue("Plone Configuration" in self.browser.contents)

    def test_language_control_panel_sidebar(self):
        self.browser.open(
            "%s/@@language-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@overview-controlpanel')

    def test_use_combined_language_codes(self):
        self.browser.open(
            "%s/@@language-controlpanel" % self.portal_url)
        self.browser.getControl('Show country-specific language variants')\
            .selected = True
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILanguageSchema)
        self.assertEqual(settings.use_combined_language_codes, True)

    def test_default_language(self):
        self.browser.open(
            "%s/@@language-controlpanel" % self.portal_url)
        self.browser.getControl('Site language').value = ['en']
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILanguageSchema)
        self.assertEqual(settings.default_language, 'en')


class LanguageRegistryIntegrationTest(unittest.TestCase):
    """Test that changes in the language registry are actually applied.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ILanguageSchema)
        self.ltool = getToolByName(self.portal, "portal_languages")

    def test_default_language(self):
        self.assertEqual(self.settings.default_language, 'en')
        self.assertEquals(self.ltool.getDefaultLanguage(), 'en')

        self.settings.default_language = 'de'

        self.assertEqual(self.settings.default_language, 'de')
        self.assertEquals(self.ltool.getDefaultLanguage(), 'de')

    def test_use_combined_language_codes(self):
        self.assertEqual(self.settings.use_combined_language_codes, False)
        self.assertEquals(self.ltool.use_combined_language_codes, False)

        self.settings.use_combined_language_codes = True

        self.assertEqual(self.settings.use_combined_language_codes, True)
        self.assertEquals(self.ltool.use_combined_language_codes, True)


class LanguageControlPanelAdapterFunctionalTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.ltool = getToolByName(self.portal, "portal_languages")
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_default_language(self):
        self.assertEqual(self.ltool.getDefaultLanguage(), 'en')
        self.browser.open(
            "%s/@@language-controlpanel" % self.portal_url)
        self.browser.getControl(
            'Site language').value = ['de']
        self.browser.getControl('Save').click()

        self.assertEqual(self.ltool.getDefaultLanguage(), 'de')

    def test_use_combined_language_codes(self):
        self.assertEqual(self.ltool.use_combined_language_codes, False)
        self.browser.open(
            "%s/@@language-controlpanel" % self.portal_url)
        self.browser.getControl(
            'Show country-specific language variants').selected = True
        self.browser.getControl('Save').click()

        self.assertEqual(self.ltool.use_combined_language_codes, True)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
