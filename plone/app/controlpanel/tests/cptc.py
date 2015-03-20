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


def generateUsers(portal):
    members = [{'username': 'DIispfuF', 'fullname': 'Kevin Hughes', 'email': 'DIispfuF@example.com'},
               {'username': 'enTHXigm', 'fullname': 'Richard Ramirez', 'email': 'enTHXigm@example.com'},
               {'username': 'q7UsYcrT', 'fullname': 'Kyle Brown', 'email': 'q7UsYcrT@example.com'},
               {'username': 'j5g0xPmr', 'fullname': 'Julian Green', 'email': 'j5g0xPmr@example.com'},
               {'username': 'o6Sx4It3', 'fullname': 'Makayla Coleman', 'email': 'o6Sx4It3@example.com'},
               {'username': 'SLUhquYa', 'fullname': 'Sean Foster', 'email': 'SLUhquYa@example.com'},
               {'username': 'nHWl3Ita', 'fullname': 'Molly Martin', 'email': 'nHWl3Ita@example.com'},
               {'username': 'xdkpCKmX', 'fullname': 'Jordan Thompson', 'email': 'xdkpCKmX@example.com'},
               {'username': 'p8H6CicB', 'fullname': 'Tyler Rivera', 'email': 'p8H6CicB@example.com'},
               {'username': 'T6vdBXbD', 'fullname': 'Megan Murphy', 'email': 'T6vdBXbD@example.com'},
               {'username': 'DohPmgIa', 'fullname': 'Gracie Diaz', 'email': 'DohPmgIa@example.com'},
               {'username': 'CqHWi65B', 'fullname': 'Rachel Morgan', 'email': 'CqHWi65B@example.com'},
               {'username': 'uHFQ7qk4', 'fullname': 'Maya Price', 'email': 'uHFQ7qk4@example.com'},
               {'username': 'BlXLQh7r', 'fullname': 'Blake Jenkins', 'email': 'BlXLQh7r@example.com'},
               {'username': 'FCrWUiSY', 'fullname': 'Owen Ramirez', 'email': 'FCrWUiSY@example.com'},
               {'username': 'bX3PqgHK', 'fullname': 'Owen Cook', 'email': 'bX3PqgHK@example.com'},
               {'username': 'sD35vVl0', 'fullname': 'Jayden Hill', 'email': 'sD35vVl0@example.com'},
               {'username': 'mfOcjXAG', 'fullname': 'Joseph Ramirez', 'email': 'mfOcjXAG@example.com'},
               {'username': 'GAJtdYbM', 'fullname': 'Nathan Young', 'email': 'GAJtdYbM@example.com'},
               {'username': 'E1OWG6bv', 'fullname': 'Kaitlyn Hernandez', 'email': 'E1OWG6bv@example.com'},
               {'username': 'BqOX2sCm', 'fullname': 'Faith Price', 'email': 'BqOX2sCm@example.com'},
               {'username': 'tyOxRnml', 'fullname': 'Sofia Williams', 'email': '5yOxRjtl@example.com'},
               {'username': 'fVcumDNl', 'fullname': 'David Sanders', 'email': 'fVcumDNl@example.com'},
               {'username': 'Ge1hqdEI', 'fullname': 'Jack Simmons', 'email': 'Ge1hqdEI@example.com'},
               {'username': 'o2CqT7kG', 'fullname': 'Cole Howard', 'email': 'o2CqT7kG@example.com'},
               {'username': 'mpGtfNl6', 'fullname': 'Rachel Miller', 'email': 'mpGtfNl6@example.com'},
               {'username': 'RGrpWiBg', 'fullname': 'Henry Patterson', 'email': 'RGrpWiBg@example.com'},
               {'username': 'Bufmi0YS', 'fullname': 'Avery Cooper', 'email': 'Bufmi0YS@example.com'},
               {'username': 'J7NvbjYd', 'fullname': 'Sydney Bennett', 'email': 'J7NvbjYd@example.com'},
               {'username': 'u5Xem8U1', 'fullname': 'Daniel Johnson', 'email': 'u5Xem8U1@example.com'},
               {'username': 'TWrMCLIo', 'fullname': 'Autumn Brooks', 'email': '0VrMCLIo@example.com'},
               {'username': 'FElYwiIr', 'fullname': 'Alexandra Nelson', 'email': 'FElYwiIr@example.com'},
               {'username': 'teK6pkhc', 'fullname': 'Brian Simmons', 'email': '0eK6pkhc@example.com'},
               {'username': 'RwAO2YPa', 'fullname': 'Gracie Adams', 'email': 'gracie@example.com'},
               {'username': 'nlBMw26i', 'fullname': 'Sydney Evans', 'email': 'nlBMw26i@example.com'},
               {'username': 'Ahr3EiRC', 'fullname': 'Emma Brown', 'email': 'Ahr3EiRC@example.com'},
               {'username': 'NhuU0Y5x', 'fullname': 'Lauren Martin', 'email': 'NhuU0Y5x@example.com'},
               {'username': 'j2R3mKQg', 'fullname': 'Isabelle Russell', 'email': 'j2R3mKQg@example.com'},
               {'username': 'qOmK0iCN', 'fullname': 'Anna Baker', 'email': 'qOmK0iCN@example.com'},
               {'username': 'uQbVOgo7', 'fullname': 'Brady Watson', 'email': 'uQbVOgo7@example.com'},
               {'username': 'oLDCaQfW', 'fullname': 'Kaitlyn Robinson', 'email': 'oLDCaQfW@example.com'},
               {'username': 'osYHeFD1', 'fullname': 'Riley Richardson', 'email': 'osYHeFD1@example.com'},
               {'username': 'i4pHduDY', 'fullname': 'Kayla Sanders', 'email': 'i4pHduDY@example.com'},
               {'username': 'BvyX6qF3', 'fullname': 'Sara Richardson', 'email': 'BvyX6qF3@example.com'},
               {'username': 'a3EpwDYj', 'fullname': 'Trinity Gonzales', 'email': 'a3EpwDYj@example.com'},
               {'username': 'JDMseWdt', 'fullname': 'Madeline Garcia', 'email': 'JDMseWdt@example.com'},
               {'username': 'lPCYBvoi', 'fullname': 'Brian Gray', 'email': 'lPCYBvoi@example.com'},
               {'username': 'AByCsRQ3', 'fullname': 'Victoria Perez', 'email': 'AByCsRQ3@example.com'},
               {'username': 'CH7uVlNy', 'fullname': 'Charles Rodriguez', 'email': '5H7uVlNy@example.com'},
               {'username': 'XYsmd7ux', 'fullname': 'Abigail Simmons', 'email': 'XYsmd7ux@example.com'},
               {'username': 'DfaA1wqC3', 'fullname': 'Émilie Richard', 'email': 'DfaA1wqC3@example.com'},
               {'username': 'NP4FMIb5', 'email': 'NP4FMIb5@example.com'}]

    regtool = getToolByName(portal, 'portal_registration')
    for member in members:
        regtool.addMember(member['username'], 'somepassword', properties=member)


def generate_user_and_groups(portal):
    generateUsers(portal)
    transaction.commit()


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
        generate_user_and_groups(self.portal)
