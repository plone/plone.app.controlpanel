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
