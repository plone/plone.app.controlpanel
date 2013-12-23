# -*- coding: utf-8 -*-
import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class BBBSitePropertiesTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties

    def test_get_property_by_getProperty(self):
        self.assertEquals(
            self.site_properties.getProperty('default_editor'),
            "TinyMCE")

    def test_get_property_by_getattr(self):
        self.assertEquals(
            getattr(self.site_properties, 'default_editor', None),
            "TinyMCE")

    def test_get_property_as_attribute(self):
        self.assertEquals(
            self.site_properties.default_editor,
            "TinyMCE")

    def test_set_property_by_manage_changeProperties(self):
        self.site_properties.manage_changeProperties(default_editor="None")
        self.assertEquals(self.site_properties.default_editor, "None")

    def test_add_property_by_manage_addProperty(self):
        self.site_properties.manage_addProperty(
            'new_property', True, 'boolean')
        self.assertEquals(self.site_properties.new_property, True)

    def test_update_property_by_updateProperty(self):
        self.site_properties._updateProperty('default_editor', 'None')
        self.assertEquals(self.site_properties.default_editor, "None")


class BBBNavPropertiesTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.navtree_properties = ptool.navtree_properties

    def test_get_property_by_getProperty(self):
        self.assertEquals(
            self.navtree_properties.getProperty('enable_wf_state_filtering'),
            False)

    def test_get_property_by_getattr(self):
        self.assertEquals(
            getattr(self.navtree_properties, 'enable_wf_state_filtering'),
            False)

    def test_get_property_as_attribute(self):
        self.assertEquals(
            self.navtree_properties.enable_wf_state_filtering,
            False)

    def test_set_property_by_manage_changeProperties(self):
        self.navtree_properties.enable_wf_state_filtering = False
        self.navtree_properties.manage_changeProperties(
            enable_wf_state_filtering=True)
        self.assertEquals(
            self.navtree_properties.enable_wf_state_filtering,
            True)

    def test_add_property_by_manage_addProperty(self):
        self.navtree_properties.enable_wf_state_filtering = False
        self.navtree_properties.manage_addProperty(
            'new_property', True, 'boolean')
        self.assertEquals(self.navtree_properties.new_property, True)

    def test_update_property_by_updateProperty(self):
        self.navtree_properties.enable_wf_state_filtering = False
        self.navtree_properties._updateProperty(
            "enable_wf_state_filtering",
            True)
        self.assertEquals(
            self.navtree_properties.enable_wf_state_filtering,
            True)
