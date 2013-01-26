import unittest
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.interfaces import IUserGroupsSettingsSchema

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class SyncPloneAppRegistryToUserGroupsSitePropertiesTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IUserGroupsSettingsSchema)

    def test_sync_many_users_property(self):
        self.assertEquals(self.site_properties.many_users, False)
        self.assertEquals(self.settings.many_users, False)
        self.settings.many_users = True
        self.assertEquals(self.site_properties.many_users, True)

    def test_sync_many_groups_property(self):
        self.assertEquals(self.site_properties.many_groups, False)
        self.assertEquals(self.settings.many_groups, False)
        self.settings.many_groups = True
        self.assertEquals(self.site_properties.many_groups, True)


class SyncUserGroupsSitePropertiesToPloneAppRegistryTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IUserGroupsSettingsSchema)

    def test_sync_many_users_property(self):
        self.assertEquals(self.site_properties.many_users, False)
        self.assertEquals(self.settings.many_users, False)
        self.site_properties.manage_changeProperties(many_users=True)
        self.assertEquals(self.settings.many_users, True)

    def test_sync_many_groups_property(self):
        self.assertEquals(self.site_properties.many_groups, False)
        self.assertEquals(self.settings.many_groups, False)
        self.site_properties.manage_changeProperties(many_groups=True)
        self.assertEquals(self.settings.many_groups, True)
