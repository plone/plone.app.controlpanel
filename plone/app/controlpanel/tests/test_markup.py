# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.registry import Registry
from plone.app.controlpanel.interfaces import IMarkupSchema

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import (
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING,
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING
)


class MarkupRegistryIntegrationTest(unittest.TestCase):
    """Test plone.app.registry based markup storage.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.registry = Registry()
        self.registry.registerInterface(IMarkupSchema)

    def test_markup_controlpanel_view(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST),
            name="markup-controlpanel"
        )
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_plone_app_registry_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            'plone.app.registry' in [a.getAction(self)['id']
            for a in self.controlpanel.listActions()]
        )

    def test_default_type_setting(self):
        self.assertTrue('default_type' in IMarkupSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'IMarkupSchema.default_type'],
            'text/html'
        )

    def test_allowed_types_setting(self):
        self.assertTrue('allowed_types' in IMarkupSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'IMarkupSchema.allowed_types'],
            ('text/html', 'text/x-web-textile')
        )


class MarkupControlPanelFunctionalTest(unittest.TestCase):
    """Make sure changes in the markup control panel are properly
    stored in plone.app.registry.
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

    def test_markup_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Markup').click()

    def test_markup_control_panel_backlink(self):
        self.browser.open(
            "%s/@@markup-controlpanel" % self.portal_url)
        self.assertTrue("Plone Configuration" in self.browser.contents)

    def test_markup_control_panel_sidebar(self):
        self.browser.open(
            "%s/@@markup-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@overview-controlpanel')

    def test_default_type(self):
        self.browser.open(
            "%s/@@markup-controlpanel" % self.portal_url)
        self.browser.getControl('Default format').value = ['text/plain']
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IMarkupSchema)
        self.assertEqual(settings.default_type, 'text/plain')

    def test_allowed_types(self):
        self.browser.open(
            "%s/@@markup-controlpanel" % self.portal_url)
        self.browser.getControl(
            name='form.widgets.allowed_types:list'
        ).value = ['text/plain']
        self.browser.getControl('Save').click()

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IMarkupSchema)
        self.assertEqual(settings.allowed_types, ('text/plain',))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
