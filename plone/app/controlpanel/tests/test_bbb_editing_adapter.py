import unittest
from plone.app.testing import setRoles
from zope.component import getAdapter
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.interfaces import IEditingSchema


class EditingControlPanelAdapterTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties

    def test_adapter_lookup(self):
        self.assertTrue(getAdapter(self.portal, IEditingSchema))

    def test_get_visible_ids_setting(self):
        self.assertEquals(self.site_properties.visible_ids, False)
        self.site_properties.visible_ids = True
        editing_settings = getAdapter(self.portal, IEditingSchema)
        self.assertEquals(editing_settings.visible_ids, True)

    def test_set_visible_ids_setting(self):
        self.assertEquals(self.site_properties.visible_ids, False)
        editing_settings = getAdapter(self.portal, IEditingSchema)
        editing_settings.visible_ids = True
        self.assertEquals(self.site_properties.visible_ids, True)

    def test_get_enable_link_integrity_checks_setting(self):
        self.assertEquals(
            self.site_properties.enable_link_integrity_checks, True)
        self.site_properties.enable_link_integrity_checks = False
        editing_settings = getAdapter(self.portal, IEditingSchema)
        self.assertEquals(editing_settings.enable_link_integrity_checks, False)

    def test_set_enable_link_integrity_checks_setting(self):
        self.assertEquals(
            self.site_properties.enable_link_integrity_checks, True)
        editing_settings = getAdapter(self.portal, IEditingSchema)
        editing_settings.enable_link_integrity_checks = False
        self.assertEquals(
            self.site_properties.enable_link_integrity_checks, False)

    def test_get_ext_editor_setting(self):
        self.assertEquals(self.site_properties.ext_editor, False)
        self.site_properties.ext_editor = True
        editing_settings = getAdapter(self.portal, IEditingSchema)
        self.assertEquals(editing_settings.ext_editor, True)

    def test_set_ext_editor_setting(self):
        self.assertEquals(self.site_properties.ext_editor, False)
        editing_settings = getAdapter(self.portal, IEditingSchema)
        editing_settings.ext_editor = True
        self.assertEquals(self.site_properties.ext_editor, True)

    def test_get_default_editor_setting(self):
        self.assertEquals(self.site_properties.default_editor, "TinyMCE")
        self.site_properties.default_editor = "None"
        editing_settings = getAdapter(self.portal, IEditingSchema)
        self.assertEquals(editing_settings.default_editor, "None")

    def test_set_default_editor_setting(self):
        self.assertEquals(self.site_properties.default_editor, "TinyMCE")
        editing_settings = getAdapter(self.portal, IEditingSchema)
        editing_settings.default_editor = "None"
        self.assertEquals(self.site_properties.default_editor, "None")

    def test_get_lock_on_ttw_edit_setting(self):
        self.assertEquals(self.site_properties.lock_on_ttw_edit, True)
        self.site_properties.lock_on_ttw_edit = False
        editing_settings = getAdapter(self.portal, IEditingSchema)
        self.assertEquals(editing_settings.lock_on_ttw_edit, False)

    def test_set_lock_on_ttw_edit_setting(self):
        self.assertEquals(self.site_properties.lock_on_ttw_edit, True)
        editing_settings = getAdapter(self.portal, IEditingSchema)
        editing_settings.lock_on_ttw_edit = False
        self.assertEquals(self.site_properties.lock_on_ttw_edit, False)
