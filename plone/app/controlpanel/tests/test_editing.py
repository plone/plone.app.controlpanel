# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import SITE_OWNER_NAME
from plone.testing.z2 import Browser
from plone.registry import Registry
from plone.app.controlpanel.browser.editing import IEditingSchema
import unittest2 as unittest

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class EditingControlPanelIntegrationTest(unittest.TestCase):
    """Tests that the editing settings are stored as plone.app.registry
    settings.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = Registry()
        self.registry.registerInterface(IEditingSchema)

    def test_editing_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="editing-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_editing_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue('EditingSettings' in [a.getAction(self)['id']
                            for a in self.controlpanel.listActions()])

    def test_visible_ids_setting(self):
        self.assertTrue('visible_ids' in IEditingSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'IEditingSchema.visible_ids'],
            False)

    def test_default_editor_setting(self):
        self.assertTrue('default_editor' in IEditingSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'IEditingSchema.default_editor'],
            'TinyMCE')

    def test_ext_editor_setting(self):
        self.assertTrue('ext_editor' in IEditingSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'IEditingSchema.ext_editor'],
            False)

    def test_enable_link_integrity_checks_setting(self):
        self.assertTrue(
            'enable_link_integrity_checks' in IEditingSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'IEditingSchema.enable_link_integrity_checks'],
            True)

    def test_lock_on_ttw_edit_setting(self):
        self.assertTrue('lock_on_ttw_edit' in IEditingSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'IEditingSchema.lock_on_ttw_edit'],
            True)


class EditingControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the editing control panel are actually
    stored in the registry.
    """

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IEditingSchema)
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization',
                'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
            )

    def test_editing_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Editing').click()

    def test_editing_control_panel_backlink(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.assertTrue("Plone Configuration" in self.browser.contents)

    def test_editing_control_panel_sidebar(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@overview-controlpanel')

    def test_visible_ids(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Show 'Short Name' on content?")\
            .selected = True
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.visible_ids, True)

    def test_default_editor(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Default editor").value = ["None"]
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.default_editor, "None")

    def test_ext_editor(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Enable External Editor feature")\
            .selected = True
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.ext_editor, True)

    def test_enable_link_integrity_checks(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Enable link integrity checks")\
            .selected = True
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.enable_link_integrity_checks, True)

    def test_lock_on_ttw_edit(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Enable locking for through-the-web edits")\
            .selected = True
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.lock_on_ttw_edit, True)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
