# -*- coding: utf-8 -*-
import unittest2 as unittest

from plone.registry import Registry
from plone.app.controlpanel.interfaces import ISearchSchema

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


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

    def test_search_controlpanel_view_is_registered(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="search-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_plone_app_registry_is_listed_in_the_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            'plone.app.registry' in [
                a.getAction(self)['id']
                for a in self.controlpanel.listActions()
            ]
        )

    def test_enable_livesearch_setting(self):
        self.assertTrue('enable_livesearch' in ISearchSchema.names())

    def test_types_not_searched(self):
        self.assertTrue('types_not_searched' in ISearchSchema.names())
