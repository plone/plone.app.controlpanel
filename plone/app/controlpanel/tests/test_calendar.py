# -*- coding: utf-8 -*-
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import SITE_OWNER_NAME
from plone.testing.z2 import Browser
from plone.registry import Registry
from plone.app.controlpanel.browser.calendar import ICalendarSchema
import unittest2 as unittest

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID, setRoles

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING


class CalendarControlPanelIntegrationTest(unittest.TestCase):
    """Tests that the calendar settings are stored as plone.app.registry
    settings.
    """

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = Registry()
        self.registry.registerInterface(ICalendarSchema)

    def test_calendar_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="calendar-controlpanel")
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_calendar_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.assertTrue(
            'CalendarSettings' in [a.getAction(self)['id']
            for a in self.controlpanel.listActions()])

    def test_firstweekday_setting(self):
        self.assertTrue('firstweekday' in ICalendarSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ICalendarSchema.firstweekday'],
            0)

    def test_calendar_states_setting(self):
        self.assertTrue('calendar_states' in ICalendarSchema.names())
        self.assertEqual(
            self.registry['plone.app.controlpanel.interfaces.' +
                          'ICalendarSchema.calendar_states'],
            ('published',))


class CalendarControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the calendar control panel are actually
    stored in the registry.
    """

    layer = PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ICalendarSchema)
        self.browser = Browser(self.app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,))

    def test_calendar_control_panel_link(self):
        self.browser.open(
            "%s/plone_control_panel" % self.portal_url)
        self.browser.getLink('Calendar').click()

    def test_calendar_control_panel_backlink(self):
        self.browser.open(
            "%s/@@calendar-controlpanel" % self.portal_url)
        self.assertTrue("Plone Configuration" in self.browser.contents)

    def test_calendar_control_panel_sidebar(self):
        self.browser.open(
            "%s/@@calendar-controlpanel" % self.portal_url)
        self.browser.getLink('Site Setup').click()
        self.assertEqual(
            self.browser.url,
            'http://nohost/plone/@@overview-controlpanel')

    def test_firstweekday(self):
        self.browser.open(
            "%s/@@calendar-controlpanel" % self.portal_url)
        self.browser.getControl("First day of week in the calendar")\
            .value = ['3']
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.firstweekday, 3)

    def test_calendar_states(self):
        self.browser.open(
            "%s/@@calendar-controlpanel" % self.portal_url)
        self.browser.getControl(name="form.widgets.calendar_states:list")\
            .value = ('private',)
        self.browser.getControl('Save').click()

        self.assertEqual(self.settings.calendar_states, ('private',))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
