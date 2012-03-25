# -*- coding: utf-8 -*-
from plone.app.controlpanel.browser.editing import IEditingSchema
import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getAdapter

from plone.app.controlpanel.browser.editing import EditingControlPanel

from zope.publisher.browser import TestRequest
from z3c.form.interfaces import IFormLayer

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class EditingControlPanelIntegrationTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_editing_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="editing-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_editing_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue('EditingSettings' in [a.getAction(self)['id']
                            for a in self.controlpanel.listActions()])


class EditingControlPanelFormTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = TestRequest(
            environ={'AUTHENTICATED_USER': 'user1'},
            form={
                'form.widgets.visible_ids': 'true',
                'form.widgets.enable_inline_editing': 'true',
                'form.widgets.enable_link_integrity_checks': 'true',
                'form.widgets.default_editor': "TinyMCE",
                'form.widgets.lock_on_ttw_edit': "true",
                'form.widgets.ext_editor': "true",
                'form.buttons.save': 'true',
            },
            skin=IFormLayer)
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties

    def test_editing_control_panel_form(self):
        editing_form = EditingControlPanel(self.portal, self.request)

        editing_form.update()

        self.assertTrue('visible_ids' in editing_form.fields.keys())
        self.assertTrue('default_editor' in editing_form.fields.keys())
        self.assertTrue('ext_editor' in editing_form.fields.keys())
        self.assertTrue('enable_inline_editing' in editing_form.fields.keys())
        self.assertTrue(
            'enable_link_integrity_checks' in editing_form.fields.keys())
        self.assertTrue('lock_on_ttw_edit' in editing_form.fields.keys())

    def test_visible_ids_setting(self):
        editing_form = EditingControlPanel(self.portal, self.request)

        editing_form.update()
        editing_form.handleSave(editing_form, "action")

        self.assertEquals(
            self.site_properties.getProperty('visible_ids'), True)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
