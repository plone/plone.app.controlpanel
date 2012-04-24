import unittest
from plone.app.testing import setRoles
from plone.app.controlpanel.interfaces import ISecuritySchema
from zope.component import getAdapter
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class SecurityControlPanelAdapterTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties

    def test_adapter_lookup(self):
        self.assertTrue(getAdapter(self.portal, ISecuritySchema))

    def test_get_enable_self_reg_setting(self):
        pass

    def test_set_enable_self_reg_setting(self):
        pass

    def test_get_enable_user_pwd_choice_setting(self):
        self.assertEquals(self.portal.validate_email, True)
        security_settings = getAdapter(self.portal, ISecuritySchema)
        self.assertEquals(security_settings.enable_user_pwd_choice, False)

    def test_set_enable_user_pwd_choice_setting(self):
        self.assertEquals(self.portal.validate_email, True)
        security_settings = getAdapter(self.portal, ISecuritySchema)
        security_settings.enable_user_pwd_choice = True
        self.assertEquals(self.portal.validate_email, False)

    def test_get_enable_user_folders_setting(self):
        pass

    def test_set_enable_user_folders_setting(self):
        pass

    def test_get_allow_anon_views_about_setting(self):
        pass

    def test_set_allow_anon_views_about_setting(self):
        pass

    def test_get_use_email_as_login_setting(self):
        pass

    def test_set_use_email_as_login_setting(self):
        pass
