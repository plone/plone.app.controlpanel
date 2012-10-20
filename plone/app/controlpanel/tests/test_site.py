# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.registry import Registry
from plone.app.controlpanel.interfaces import ISiteSchema

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class SiteRegistryIntegrationTest(unittest.TestCase):
    """Test that the site settings are stored as plone.app.registry
    settings.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.registry = Registry()
        self.registry.registerInterface(ISiteSchema)

    def test_site_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="site-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_plone_app_registry_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            'plone.app.registry' in [a.getAction(self)['id']
            for a in self.controlpanel.listActions()]
        )

    def test_site_title_setting(self):
        self.assertTrue('site_title' in ISiteSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISiteSchema.site_title'],
            u"")

    def test_site_description_setting(self):
        self.assertTrue('site_description' in ISiteSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISiteSchema.site_description'],
            u"")

    def test_exposeDCMetaTags_setting(self):
        self.assertTrue('exposeDCMetaTags' in ISiteSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISiteSchema.exposeDCMetaTags'],
            False)

    def test_webstats_js_setting(self):
        self.assertTrue('webstats_js' in ISiteSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISiteSchema.webstats_js'],
            u"")

    def test_enable_sitemap_setting(self):
        self.assertTrue('enable_sitemap' in ISiteSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ISiteSchema.enable_sitemap'],
            False)


class SiteControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the site control panel are actually
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

    def test_site_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Site').click()

    def test_site_control_panel_backlink(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.assertTrue("Plone Configuration" in self.browser.contents)

    def test_site_control_panel_sidebar(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@overview-controlpanel')

    def test_site_title(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getControl('Site title').value = u"Plone Site"
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema)
        self.assertEqual(settings.site_title, u"Plone Site")

    def test_site_description(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getControl('Site title').value = u"Plone Site"
        self.browser.getControl('Site description').value = \
            u"This is a Plone site."
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema)
        self.assertEqual(settings.site_description, u"This is a Plone site.")

    def test_exposeDCMetaTags(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getControl('Site title').value = u"Plone Site"
        self.browser.getControl('Expose Dublin Core metadata').selected = True
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema)
        self.assertEqual(settings.exposeDCMetaTags, True)

    def test_enable_sitemap(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getControl('Site title').value = u"Plone Site"
        self.browser.getControl('Expose sitemap.xml.gz').selected = True
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema)
        self.assertEqual(settings.enable_sitemap, True)

    def test_webstats_js(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getControl('Site title').value = u"Plone Site"
        self.browser.getControl(name='form.widgets.webstats_js').value = \
            u"<script>a=1</script>"
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema)
        self.assertEqual(settings.webstats_js, u"<script>a=1</script>")


class SiteRegistryIntegrationTest(unittest.TestCase):
    """Test that changes in the site registry are actually applied.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISiteSchema)
        self.site_properties = self.portal.portal_properties.site_properties
        self.mtool = getToolByName(self.portal, "portal_membership")

    def test_site_title(self):
        self.assertEqual(self.settings.site_title, u"")
        self.assertEqual(self.portal.get("site_title", None), None)

        self.settings.site_title = u"Plone Site"

        self.assertEqual(self.settings.site_title, u"Plone Site")
        self.assertEqual(self.portal.site_title, u"Plone Site")

    def test_site_description(self):
        self.assertEqual(self.settings.site_description, u"")
        self.assertEqual(self.portal.get("site_description", None), None)

        self.settings.site_description = u"Plone Site Description"

        self.assertEqual(
            self.settings.site_description,
            u"Plone Site Description")
        self.assertEqual(
            self.portal.site_description,
            u"Plone Site Description")

    # XXX: Todo


class SiteControlPanelAdapterFunctionalTest(unittest.TestCase):

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

    def test_site_title(self):
        self.assertEqual(self.portal.get("site_title", None), None)
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getControl(
            'Site title').value = u"Plone Site"
        self.browser.getControl('Save').click()

        self.assertEqual(self.portal.site_title, u"Plone Site")


    # XXX: Todo


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
