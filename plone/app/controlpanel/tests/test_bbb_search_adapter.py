# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.controlpanel.interfaces import ISearchSchema

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class SearchControlPanelAdapterFunctionalTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISearchSchema)
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_enable_livesearch(self):
        self.assertEqual(self.settings.enable_livesearch, True)
        self.browser.open(
            "%s/@@search-controlpanel" % self.portal_url)
        self.browser.getControl(
            'Enable LiveSearch').selected = False
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.enable_livesearch, False)

    def test_types_not_searched_contains_unselected_types(self):
        self.browser.open(
            "%s/@@search-controlpanel" % self.portal_url)
        self.browser.getControl(name='form.widgets.types_not_searched:list')\
            .value = ['Document']
        self.browser.getControl('Save').click()
        self.assertTrue('Event' in self.settings.types_not_searched)

    def test_types_not_searched_does_not_contain_selected_types(self):
        self.browser.open(
            "%s/@@search-controlpanel" % self.portal_url)
        self.browser.getControl(name='form.widgets.types_not_searched:list')\
            .value = ['Event']
        self.browser.getControl('Save').click()
        self.assertFalse('Event' in self.settings.types_not_searched)
