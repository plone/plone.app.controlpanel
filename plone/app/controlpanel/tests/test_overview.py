from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

import mock
import unittest


class MockSettings(mock.Mock):
    portal_timezone = None


class MockUtil(mock.Mock):
    forInterface = MockSettings


class MockSettings2(mock.Mock):
    portal_timezone = "Europe/Amsterdam"


class MockUtil2(mock.Mock):
    forInterface = MockSettings2


class TestControlPanel(unittest.TestCase):

    layer = PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    @mock.patch('plone.app.controlpanel.overview.queryUtility', new=MockUtil)
    def test_timezone_warning(self):
        mocked = mock.Mock()
        modules = {
            'plone': mocked,
            'plone.app': mocked.module,
            'plone.app.event': mocked.module.module,
            'plone.app.event.interfaces': mocked.module.module.module,
        }
        with mock.patch.dict('sys.modules', modules):
            view = self.portal.restrictedTraverse('@@overview-controlpanel')
            # if portal_timezone isn't set, return True
            self.assertTrue(view.timezone_warning())

    @mock.patch('plone.app.controlpanel.overview.queryUtility', new=MockUtil2)
    def test_no_timezone_warning(self):
        mocked = mock.Mock()
        modules = {
            'plone': mocked,
            'plone.app': mocked.module,
            'plone.app.event': mocked.module.module,
            'plone.app.event.interfaces': mocked.module.module.module,
        }
        with mock.patch.dict('sys.modules', modules):
            view = self.portal.restrictedTraverse('@@overview-controlpanel')
            # if portal_timezone isn't set, return True
            self.assertFalse(view.timezone_warning())
