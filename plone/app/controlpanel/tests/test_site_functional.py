# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from zope.component import getUtility
from zope.component import getMultiAdapter
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


class SiteControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the site control panel are actually
    stored in the registry.
    """

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
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

    def test_site_title_is_stored_in_registry(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getControl('Site title').value = u"My Site"
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema)
        self.assertEqual(settings.site_title, u"My Site")

    def test_site_title_can_be_looked_up_by_plone_portal_state(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getControl('Site title').value = u"My Site"
        self.browser.getControl('Save').click()

        portal_state = getMultiAdapter(
            (self.portal, self.request),
            name=u'plone_portal_state'
        )
        self.assertEqual(portal_state.portal_title(), u'My Site')

    @unittest.skip("XXX: TODO! We have to patch CMFDefault for this.")
    def test_site_title_can_be_looked_up_by_portal_title(self):
        self.browser.open(
            "%s/@@site-controlpanel" % self.portal_url)
        self.browser.getControl('Site title').value = u"My Site"
        self.browser.getControl('Save').click()

        self.assertEqual(self.portal.title, u'My Site')
        self.assertEqual(self.portal.Title(), u'My Site')

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
