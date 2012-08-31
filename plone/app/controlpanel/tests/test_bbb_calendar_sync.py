import unittest
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel.interfaces import ICalendarSchema

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class SyncPloneAppRegistryToCalendarPropertiesTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.ctool = getToolByName(self.portal, 'portal_calendar')
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(ICalendarSchema)

    def test_sync_firstweekday_property(self):
        self.assertEquals(self.ctool.firstweekday, 0)
        self.assertEquals(self.settings.firstweekday, 0)
        self.settings.firstweekday = 4
        self.assertEquals(self.ctool.firstweekday, 4)

    def test_sync_calendar_states_property(self):
        self.assertEquals(self.ctool.calendar_states, ('published',))
        self.assertEquals(self.settings.calendar_states, ('published',))
        self.settings.calendar_states = ('private',)
        self.assertEquals(self.ctool.calendar_states, ('private',))


class SyncCalendarPropertiesToPloneAppRegistryTest(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.ctool = getToolByName(self.portal, 'portal_calendar')
        registry = queryUtility(IRegistry)
        self.settings = registry.forInterface(ICalendarSchema)

    def test_firstweekday_property(self):
        self.assertEquals(self.ctool.firstweekday, 0)
        self.assertEquals(self.settings.firstweekday, 0)
        self.ctool.edit_configuration(
            ('Event'),
            True,
            firstweekday=5)
        self.assertEquals(self.ctool.firstweekday, 5)
        self.assertEquals(self.settings.firstweekday, 5)

    def test_calendar_states_property(self):
        self.assertEquals(self.ctool.calendar_states, ('published',))
        self.assertEquals(self.settings.calendar_states, ('published',))
        self.ctool.edit_configuration(
            ('Event'),
            True,
            show_states=('private',))
        self.assertEquals(self.ctool.calendar_states, ('private',))
        self.assertEquals(self.settings.calendar_states, ('private',))
