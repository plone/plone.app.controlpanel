# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import SITE_OWNER_NAME
from plone.testing.z2 import Browser
from plone.app.controlpanel.browser.editing import IEditingSchema
from plone.app.linkintegrity.interfaces import ILinkIntegrityInfo

import unittest2 as unittest

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class EditingControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the editing control panel are actually
    stored in the registry.
    """

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IEditingSchema)
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
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

    @unittest.skip("TODO: Not implemented yet.")
    def test_visible_ids_active(self):
        pass

    def test_default_editor(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Default editor").value = ["None"]
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.default_editor, "None")

    @unittest.skip("TODO: Not implemented yet.")
    def test_default_editor_active(self):
        pass

    def test_ext_editor(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Enable External Editor feature")\
            .selected = True
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.ext_editor, True)

    @unittest.skip("TODO: Not implemented yet.")
    def test_ext_editor_active(self):
        pass

    def test_enable_link_integrity_checks(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Enable link integrity checks")\
            .selected = True
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.enable_link_integrity_checks, True)

    def test_enable_link_integrity_checks_active(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Enable link integrity checks")\
            .selected = True
        self.browser.getControl('Save').click()

        self.assertTrue(
            ILinkIntegrityInfo(self.request).integrityCheckingEnabled())

    def test_lock_on_ttw_edit(self):
        self.browser.open(
            "%s/@@editing-controlpanel" % self.portal_url)
        self.browser.getControl("Enable locking for through-the-web edits")\
            .selected = True
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.lock_on_ttw_edit, True)

    @unittest.skip("TODO: Not implemented yet.")
    def test_lock_on_ttw_edit_active(self):
        pass