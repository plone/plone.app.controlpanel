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


def simplify_white_space(text):
    """For easier testing we replace all white space with one space.

    And we remove white space around '<' and '>'.

    So this:

      <p
          id="foo"> Bar
      </p>

    becomes this:

      <p id="foo">Bar</p>
    """
    text = re.sub('\s*<\s*', '<', text)
    text = re.sub('\s*>\s*', '>', text)
    text = re.sub('\s+', ' ', text)
    return text


class ControlPanelFixture(PloneTestCaseFixture):

    def setUpPloneSite(self, portal):
        super(ControlPanelFixture, self).setUpPloneSite(portal)
        portal.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])


CP_FIXTURE = ControlPanelFixture()
CP_FUNCTIONAL_LAYER = testing.FunctionalTesting(
    bases=(CP_FIXTURE,), name='ControlPanel:Functional')


class ControlPanelTestCase(FunctionalTestCase):
    """base test case with convenience methods for all control panel tests"""

    layer = CP_FUNCTIONAL_LAYER

    def simplify_white_space(self, text):
        return simplify_white_space(text)


class UserGroupsControlPanelTestCase(ControlPanelTestCase):
    """user/groups-specific test case"""

    def afterSetUp(self):
        super(UserGroupsControlPanelTestCase, self).afterSetUp()
        members = [
            {'username': 'DIispfuF', 'fullname': 'Kevin Hughes', 'email': 'DIispfuF@example.com'},
            {'username': 'NP4FMIb5', 'email': 'NP4FMIb5@example.com'}
        ]
        regtool = getToolByName(self.portal, 'portal_registration')
        for member in members:
            regtool.addMember(
                member['username'],
                'somepassword',
                properties=member
            )
        transaction.commit()

