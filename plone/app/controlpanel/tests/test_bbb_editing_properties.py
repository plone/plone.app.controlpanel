import unittest
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.interfaces import IEditingSchema

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class EditingPropertiesBBBTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(IEditingSchema)

    def test_set_visible_ids_property(self):
        self.assertEquals(self.site_properties.visible_ids, False)
        self.assertEquals(self.settings.visible_ids, False)
        self.settings.visible_ids = True
        self.assertEquals(self.site_properties.visible_ids, True)

    def test_set_enable_inline_editing_property(self):
        self.assertEquals(self.site_properties.enable_inline_editing, False)
        self.assertEquals(self.settings.enable_inline_editing, False)
        self.settings.enable_inline_editing = True
        self.assertEquals(self.site_properties.enable_inline_editing, True)

    def test_set_enable_link_integrity_checks_property(self):
        self.assertEquals(
            self.site_properties.enable_link_integrity_checks, True)
        self.assertEquals(
            self.settings.enable_link_integrity_checks, True)
        self.settings.enable_link_integrity_checks = False
        self.assertEquals(
            self.site_properties.enable_link_integrity_checks, False)

    def test_set_ext_editor_property(self):
        self.assertEquals(self.site_properties.ext_editor, False)
        self.assertEquals(self.settings.ext_editor, False)
        self.settings.ext_editor = True
        self.assertEquals(self.site_properties.ext_editor, True)

    def test_set_default_editor_property(self):
        self.assertEquals(self.site_properties.default_editor, 'TinyMCE')
        self.assertEquals(self.settings.default_editor, 'TinyMCE')
        self.settings.default_editor = 'None'
        self.assertEquals(self.site_properties.default_editor, 'None')

    def test_set_lock_on_ttw_edit_property(self):
        self.assertEquals(self.site_properties.lock_on_ttw_edit, True)
        self.assertEquals(self.settings.lock_on_ttw_edit, True)
        self.settings.lock_on_ttw_edit = False
        self.assertEquals(self.site_properties.lock_on_ttw_edit, False)
