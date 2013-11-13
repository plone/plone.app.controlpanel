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


class NavigationControlPanelAdapterFunctionalTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.registry = Registry()
        self.registry.registerInterface(INavigationSchema)
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

        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'INavigationSchema.generate_tabs'],
            True)
