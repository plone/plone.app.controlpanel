import unittest
from plone.app.testing import setRoles
from plone.app.controlpanel.interfaces import IMaintenanceSchema
from zope.component import getAdapter
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class MaintenanceControlPanelAdapterTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        ptool = getToolByName(self.portal, 'portal_properties')
        self.site_properties = ptool.site_properties

    def test_adapter_lookup(self):
        self.assertTrue(getAdapter(self.portal, IMaintenanceSchema))

    def test_get_days_setting(self):
        self.assertEqual(self.site_properties.number_of_days_to_keep, 7)
        maintenance_settings = getAdapter(self.portal, IMaintenanceSchema)
        self.assertEqual(maintenance_settings.days, 7)

    def test_set_days_setting(self):
        self.assertEqual(self.site_properties.number_of_days_to_keep, 7)
        maintenance_settings = getAdapter(self.portal, IMaintenanceSchema)
        maintenance_settings.days = 13
        self.assertEqual(self.site_properties.number_of_days_to_keep, 13)
