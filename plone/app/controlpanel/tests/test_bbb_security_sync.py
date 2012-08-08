import unittest
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.interfaces import ISecuritySchema

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class TestSyncPloneAppRegistryToSecurityPortalProperties(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.mtool = getToolByName(self.portal, "portal_membership")
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(ISecuritySchema)

    def test_sync_enable_self_reg(self):
        self.assertTrue(
            {'selected': 'SELECTED', 'name': 'Anonymous'} not in
            self.portal.rolesOfPermission(permission='Add portal member'))
        self.assertEqual(self.settings.enable_self_reg, False)
        self.settings.enable_self_reg = True
        self.assertTrue(
            {'selected': 'SELECTED', 'name': 'Anonymous'} in
            self.portal.rolesOfPermission(permission='Add portal member'))

    def test_sync_enable_user_pwd_choice(self):
        self.assertEqual(self.portal.validate_email, True)
        self.assertEqual(self.settings.enable_user_pwd_choice, False)
        self.settings.enable_user_pwd_choice = True
        self.assertEqual(self.portal.validate_email, False)

    def test_sync_enable_user_folders(self):
        self.assertEqual(self.mtool.getMemberareaCreationFlag(), False)
        self.assertEqual(self.settings.enable_user_folders, False)
        self.settings.enable_user_folders = True
        self.assertEqual(self.mtool.getMemberareaCreationFlag(), True)

    def test_sync_allow_anon_views_about(self):
        self.assertEqual(self.site_properties.allowAnonymousViewAbout, False)
        self.assertEqual(self.settings.allow_anon_views_about, False)
        self.settings.allow_anon_views_about = True
        self.assertEqual(self.site_properties.allowAnonymousViewAbout, True)

    def test_sync_use_email_as_login(self):
        self.assertEqual(self.site_properties.use_email_as_login, False)
        self.assertEqual(self.settings.use_email_as_login, False)
        self.settings.use_email_as_login = True
        self.assertEqual(self.site_properties.use_email_as_login, True)
