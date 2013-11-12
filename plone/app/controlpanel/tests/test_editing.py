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
