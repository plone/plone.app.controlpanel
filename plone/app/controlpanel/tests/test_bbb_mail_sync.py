from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
import unittest
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.interfaces import IMailSchema

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class TestSyncPloneAppRegistryToMailhostProperties(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IMailSchema)
        self.mailhost = getToolByName(self.portal, "MailHost")

    def test_sync_smtp_host(self):
        self.assertEqual(self.mailhost.smtp_host, "")
        self.assertEqual(self.settings.smtp_host, u"localhost")
        self.settings.smtp_host = u"http://myhost.com"
        self.assertEqual(self.mailhost.smtp_host, "http://myhost.com")

    def test_sync_smtp_port(self):
        self.assertEqual(self.mailhost.smtp_port, 25)
        self.assertEqual(self.settings.smtp_port, 25)
        self.settings.smtp_port = 2525
        self.assertEqual(self.mailhost.smtp_port, 2525)

    def test_sync_smtp_userid(self):
        self.assertEqual(self.mailhost.smtp_uid, "")
        self.assertEqual(self.settings.smtp_userid, None)
        self.settings.smtp_userid = u"johndoe"
        self.assertEqual(self.mailhost.smtp_uid, u"johndoe")

    def test_sync_smtp_pass(self):
        self.assertEqual(self.mailhost.smtp_pwd, "")
        self.assertEqual(self.settings.smtp_pass, None)
        self.settings.smtp_pass = u"secret"
        self.assertEqual(self.mailhost.smtp_pwd, u"secret")

    def test_sync_email_form_name(self):
        self.assertEqual(getUtility(ISiteRoot).email_from_name, "")
        self.assertEqual(self.settings.email_from_name, None)
        self.settings.email_from_name = u"Site Administrator"
        self.assertEqual(
            getUtility(ISiteRoot).email_from_name,
            u"Site Administrator")

    def test_sync_email_form_address(self):
        self.assertEqual(getUtility(ISiteRoot).email_from_address, "")
        self.assertEqual(self.settings.email_from_address, None)
        self.settings.email_from_address = "admin@plone.org"
        self.assertEqual(
            getUtility(ISiteRoot).email_from_address,
            "admin@plone.org")


class TestSyncMailhostPropertiesToPloneAppRegistry(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IMailSchema)
        self.mailhost = getToolByName(self.portal, "MailHost")

    def test_sync_smtp_host(self):
        self.assertEqual(self.mailhost.smtp_host, "")
        self.assertEqual(self.settings.smtp_host, u"localhost")
        self.mailhost.manage_makeChanges(
            "Plone Mail Host",
            smtp_port=25,
            smtp_host="http://myhost.com")
        self.assertEqual(self.mailhost.smtp_host, "http://myhost.com")
        self.assertEqual(self.settings.smtp_host, "http://myhost.com")

    def test_sync_smtp_port(self):
        self.assertEqual(self.mailhost.smtp_port, 25)
        self.assertEqual(self.settings.smtp_port, 25)
        self.mailhost.manage_makeChanges(
            "Plone Mail Host",
            smtp_port=2525,
            smtp_host="http://myhost.com")
        self.assertEqual(self.mailhost.smtp_port, 2525)
        self.assertEqual(self.settings.smtp_port, 2525)

    def test_sync_smtp_userid(self):
        self.assertEqual(self.mailhost.smtp_uid, "")
        self.assertEqual(self.settings.smtp_userid, None)
        self.mailhost.manage_makeChanges(
            "Plone Mail Host",
            smtp_port=2525,
            smtp_host="http://myhost.com",
            smtp_uid=u"johndoe")
        self.assertEqual(self.mailhost.smtp_uid, u"johndoe")
        self.assertEqual(self.settings.smtp_userid, u"johndoe")

    def test_sync_smtp_pass(self):
        self.assertEqual(self.mailhost.smtp_pwd, "")
        self.assertEqual(self.settings.smtp_pass, None)
        self.mailhost.manage_makeChanges(
            "Plone Mail Host",
            smtp_port=2525,
            smtp_host="http://myhost.com",
            smtp_uid=u"johndoe",
            smtp_pwd=u"secret")
        self.assertEqual(self.mailhost.smtp_pwd, u"secret")
        self.assertEqual(self.settings.smtp_pass, u"secret")

    def test_sync_email_form_name(self):
        self.assertEqual(self.portal.email_from_name, "")
        self.assertEqual(self.settings.email_from_name, None)
        self.portal.manage_changeProperties(
            email_from_name=u"Site Administrator")
        self.assertEqual(
            getUtility(ISiteRoot).email_from_name,
            u"Site Administrator")
        self.assertEqual(self.settings.email_from_name, u"Site Administrator")

    def test_sync_email_form_address(self):
        self.assertEqual(self.portal.email_from_address, "")
        self.assertEqual(self.settings.email_from_address, None)
        self.portal.manage_changeProperties(
            email_from_address="admin@plone.org")
        self.assertEqual(
            getUtility(ISiteRoot).email_from_address,
            "admin@plone.org")
        self.assertEqual(self.settings.email_from_address, "admin@plone.org")
