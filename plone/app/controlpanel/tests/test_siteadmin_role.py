import unittest2 as unittest

from plone.app.controlpanel.testing import \
    PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING


class TestSiteAdministratorRoleFunctional(unittest.TestCase):

    layer = PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_rewrite_old_tests(self):
        # XXX: Re-write tests from master here
        pass
