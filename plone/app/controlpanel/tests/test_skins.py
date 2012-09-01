# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import SITE_OWNER_NAME
from plone.testing.z2 import Browser
from plone.registry import Registry
from plone.app.controlpanel.browser.skins import ISkinsSchema
import unittest2 as unittest

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class SkinsControlPanelIntegrationTest(unittest.TestCase):
    """Tests that the skins settings are stored as plone.app.registry
    settings.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = Registry()
        self.registry.registerInterface(ISkinsSchema)

    def test_skins_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="skins-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_skins_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            'skins' in [a.getAction(self)['id']
            for a in self.controlpanel.listActions()])

    def test_theme_setting(self):
        self.assertTrue('theme' in ISkinsSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISkinsSchema.theme'],
            "Sunburst Theme")

    def test_mark_special_links(self):
        self.assertTrue('theme' in ISkinsSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISkinsSchema.mark_special_links'],
            True)

    def test_ext_links_open_new_window(self):
        self.assertTrue('theme' in ISkinsSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISkinsSchema.ext_links_open_new_window'],
            False)

    def test_icon_visibility(self):
        self.assertTrue('theme' in ISkinsSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISkinsSchema.icon_visibility'],
            "enabled")

    def test_use_popups(self):
        self.assertTrue('theme' in ISkinsSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISkinsSchema.use_popups'],
            True)


class SkinsControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the skins control panel are actually
    stored in the registry.
    """

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISkinsSchema)
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,))

    def test_skins_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Themes').click()
        self.assertTrue(
            self.browser.url,
            'http://nohost/plone/@@skins-controlpanel')

    def test_skins_control_panel_backlink(self):
        self.browser.open(
            "%s/@@skins-controlpanel" % self.portal_url)
        self.assertTrue("Plone Configuration" in self.browser.contents)

    def test_skins_control_panel_sidebar(self):
        self.browser.open(
            "%s/@@skins-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@overview-controlpanel')

    def test_theme(self):
        self.browser.open(
            "%s/@@skins-controlpanel" % self.portal_url)
        self.browser.getControl("Default theme")\
            .value = ["Plone Default"]
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.theme, "Plone Default")

    def test_mark_special_links(self):
        self.browser.open(
            "%s/@@skins-controlpanel" % self.portal_url)
        self.browser.getControl("Mark external links")\
            .selected = False
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.mark_special_links, False)

    def test_ext_links_open_new_window(self):
        self.browser.open(
            "%s/@@skins-controlpanel" % self.portal_url)
        self.browser.getControl("External links open in new window")\
            .selected = True
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.ext_links_open_new_window, True)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
