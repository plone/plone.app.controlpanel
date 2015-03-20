# -*- coding: utf-8 -*-
"""Base class for control panel test cases.

This is in a separate module because it's potentially useful to other
packages which register controlpanels.
"""

import re
import transaction

from plone.app.testing.bbb import PloneTestCase as FunctionalTestCase
from plone.app.testing.bbb import PloneTestCaseFixture
from plone.app import testing
from Products.CMFCore.utils import getToolByName


class ControlPanelFixture(PloneTestCaseFixture):

    def setUpPloneSite(self, portal):
        super(ControlPanelFixture, self).setUpPloneSite(portal)
        portal.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])


CP_FIXTURE = ControlPanelFixture()
CP_FUNCTIONAL_LAYER = testing.FunctionalTesting(
    bases=(CP_FIXTURE,), name='ControlPanel:Functional')


class UserGroupsControlPanelTestCase(FunctionalTestCase):
    """user/groups-specific test case"""

    layer = CP_FUNCTIONAL_LAYER

    def afterSetUp(self):
        super(UserGroupsControlPanelTestCase, self).afterSetUp()
        members = [
            {
              'username': 'DIispfuF',
              'fullname': 'Kevin Hughes',
              'email': 'DIispfuF@example.com'
            },
        ]
        regtool = getToolByName(self.portal, 'portal_registration')
        for member in members:
            regtool.addMember(
                member['username'],
                'somepassword',
                properties=member
            )
        transaction.commit()
