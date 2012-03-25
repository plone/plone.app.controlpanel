# -*- coding: utf-8 -*-
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
from plone.app.controlpanel.browser.mail import IMailSchema
import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getAdapter

from plone.app.controlpanel.browser.mail import MailControlPanel

from zope.publisher.browser import TestRequest
from z3c.form.interfaces import IFormLayer

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class MailControlPanelIntegrationTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_mail_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="mail-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_plone_app_registry_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue('plone.app.registry' in [a.getAction(self)['id']
                            for a in self.controlpanel.listActions()])


class MailControlPanelFormTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = TestRequest(
            environ={'AUTHENTICATED_USER': 'user1'},
            form={
                'form.widgets.smtp_host': u'localhost',
                'form.widgets.smtp_port': u'25',
                'form.widgets.smtp_userid': u'johndoe',
                'form.widgets.smtp_pass': u'secret',
                'form.widgets.email_from_name': u"Plone Site",
                'form.widgets.email_from_address': "plone@plone.org",
            },
            skin=IFormLayer)
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties

    def test_mail_control_panel_form(self):
        mail_form = MailControlPanel(self.portal, self.request)

        #mail_form.update()

        #self.assertTrue('smtp_host' in mail_form.fields.keys())
        #self.assertTrue('smtp_port' in mail_form.fields.keys())
        #self.assertTrue('smtp_userid' in mail_form.fields.keys())
        #self.assertTrue('smtp_pass' in mail_form.fields.keys())
        #self.assertTrue('email_from_name' in mail_form.fields.keys())
        #self.assertTrue('email_from_address' in mail_form.fields.keys())

    def test_smtp_host_setting(self):
        mail_form = MailControlPanel(self.portal, self.request)

        #mail_form.update()
        #mail_form.handleSave(mail_form, "action")

        #self.assertEquals(
        #    self.portal.getProperty('smtp_host'), True)


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
        self.assertEquals(self.mailhost.smtp_host, "")
        self.mailhost.smtp_host = u"localhost"
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.smtp_host, u"localhost")

    def test_set_smtp_host_setting(self):
        self.assertEquals(self.mailhost.smtp_host, u"")
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.smtp_host = u"localhost"
        self.assertEquals(self.mailhost.smtp_host, u"localhost")

    def test_get_smtp_port_setting(self):
        self.assertEquals(self.portal.getProperty("smtp_port"), None)
        self.portal.smtp_port = 25
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.smtp_port, 25)

    def test_set_smtp_port_setting(self):
        self.assertEquals(self.mailhost.smtp_port, 25)
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.smtp_port = 42
        self.assertEquals(self.mailhost.smtp_port, 42)

    def test_get_smtp_userid_setting(self):
        self.assertEquals(
            self.portal.getProperty("smtp_userid"), None)
        self.portal.smtp_userid = u"johndoe"
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.smtp_userid, u"johndoe")

    def test_set_smtp_userid_setting(self):
        self.assertEquals(self.mailhost.smtp_uid, "")
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.smtp_userid = "johndoe"
        mailhost = getToolByName(self.portal, 'MailHost')
        self.assertEquals(
            getattr(mailhost, 'smtp_uid'), "johndoe")

    def test_get_smtp_pass_setting(self):
        self.assertEquals(self.mailhost.smtp_pwd, "")
        self.portal.smtp_pass = "secret"
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.smtp_pass, "secret")

    def test_set_smtp_pass_setting(self):
        self.assertEquals(self.mailhost.smtp_pwd, "")
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.smtp_pass = "secret"
        self.assertEquals(self.mailhost.smtp_pwd, "secret")

    def test_get_email_from_name_setting(self):
        self.assertEquals(self.portal.getProperty("email_from_name"), "")
        self.portal.email_from_name = u"Plone Site"
        mail_settings = getAdapter(self.portal, IMailSchema)
        self.assertEquals(mail_settings.email_from_name, u"Plone Site")

    def test_set_email_from_name_setting(self):
        self.assertEquals(self.portal.getProperty("email_from_name"), "")
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.email_from_name = u"Plone Site"
        self.assertEquals(
            getUtility(ISiteRoot).email_from_name, u"Plone Site")

    def test_get_email_from_address_setting(self):
        self.assertEquals(self.portal.getProperty("email_from_address"), "")
        self.portal.email_from_address = "plone@plone.org"
        self.assertEquals(
            getUtility(ISiteRoot).email_from_address, "plone@plone.org")

    def test_set_email_from_address_setting(self):
        self.assertEquals(self.portal.getProperty("email_from_address"), "")
        mail_settings = getAdapter(self.portal, IMailSchema)
        mail_settings.email_from_address = "plone@plone.org"
        self.assertEquals(
            getUtility(ISiteRoot).email_from_address, "plone@plone.org")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
