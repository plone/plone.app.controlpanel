import unittest
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.controlpanel.interfaces import ISiteSchema

from plone.app.testing import setRoles
from zope.component import getAdapter
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.interfaces import ISiteSchema


class SiteControlPanelAdapterTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISiteSchema)

    def test_adapter_lookup(self):
        self.assertTrue(getAdapter(self.portal, ISiteSchema))

    def test_site_title_unicode(self):
        site_settings_adapter = getAdapter(self.portal, ISiteSchema)
        site_settings_adapter.site_title = u'Lorem Ipsum'
        self.assertEquals(
            site_settings_adapter.site_title, u'Lorem Ipsum')

    def test_site_title_string(self):
        site_settings_adapter = getAdapter(self.portal, ISiteSchema)
        site_settings_adapter.site_title = 'Lorem Ipsum'
        self.assertEquals(
            site_settings_adapter.site_title, u'Lorem Ipsum')

    def test_webstats_js_unicode(self):
        self.assertEqual(self.settings.webstats_js, u'')
        site_settings_adapter = getAdapter(self.portal, ISiteSchema)
        site_settings_adapter.webstats_js = u'Lorem Ipsum'
        self.assertEquals(
            site_settings_adapter.webstats_js, u'Lorem Ipsum')

    def test_webstats_js_string(self):
        self.assertEqual(self.settings.webstats_js, u'')
        site_settings_adapter = getAdapter(self.portal, ISiteSchema)
        site_settings_adapter.webstats_js = 'Lorem Ipsum'
        self.assertEquals(
            site_settings_adapter.webstats_js, u'Lorem Ipsum')
