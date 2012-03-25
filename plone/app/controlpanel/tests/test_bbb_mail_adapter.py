import unittest
from plone.app.testing import setRoles
from plone.app.controlpanel.browser.mail import IMailSchema
from zope.component import getAdapter
from zope.component import getUtility
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class MailControlPanelAdapterTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties
        self.mailhost = getToolByName(self.portal, 'MailHost')

    def test_get_smtp_host_setting(self):
        self.mailhost.smtp_host = u"localhost"
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.smtp_host, u"localhost")

    def test_set_smtp_host_setting(self):
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.smtp_host = u"localhost"
        self.assertEquals(self.mailhost.smtp_host, u"localhost")

    def test_get_smtp_port_setting(self):
        self.mailhost.smtp_port = 41
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.smtp_port, 41)

    def test_set_smtp_port_setting(self):
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.smtp_port = 42
        self.assertEquals(self.mailhost.smtp_port, 42)

    def test_get_smtp_userid_setting(self):
        self.mailhost.smtp_userid = "johndoe"
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.smtp_userid, "johndoe")

    def test_set_smtp_userid_setting(self):
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.smtp_userid = "johndoe"
        self.assertEquals(
            self.mailhost.smtp_userid, "johndoe")

    def test_get_smtp_pass_setting(self):
        self.mailhost.smtp_pass = "secret"
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.smtp_pass, "secret")

    def test_set_smtp_pass_setting(self):
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.smtp_pass = "secret"
        self.assertEquals(self.mailhost.smtp_pass, "secret")

    def test_get_email_from_name_setting(self):
        self.portal.email_from_name = u"Plone Site"
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.email_from_name, u"Plone Site")

    def test_set_email_from_name_setting(self):
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.email_from_name = u"Plone Site"
        self.assertEquals(
            getUtility(ISiteRoot).email_from_name, u"Plone Site")

    def test_get_email_from_address_setting(self):
        self.portal.email_from_address = "plone@plone.org"
        self.assertEquals(
            getUtility(ISiteRoot).email_from_address, "plone@plone.org")

    def test_set_email_from_address_setting(self):
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.email_from_address = "plone@plone.org"
        self.assertEquals(
            getUtility(ISiteRoot).email_from_address, "plone@plone.org")
