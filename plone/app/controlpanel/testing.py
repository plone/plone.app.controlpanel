# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import applyProfile

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig


class PloneAppControlpanel(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.app.controlpanel
        xmlconfig.file('configure.zcml',
                       plone.app.controlpanel,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.controlpanel:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        # Install into Plone site using portal_setup
        #self.generateMemberarea(portal)
        self.generateUsers(portal)
        self.generateGroups(portal)

    def generateMemberarea(self, portal):
        portal.invokeFactory("Folder", "Members")
        mtool = getToolByName(portal, "portal_membership")
        mtool.setMemberAreaType("Folder")
        if not mtool.getMemberareaCreationFlag():
            mtool.setMemberareaCreationFlag()
        #mtool.createMemberarea("admin")

    def generateGroups(self, portal):
        groupsTool = getToolByName(portal, 'portal_groups')
        groupsTool.addGroup('group1', [], [], title="Group 1")
        groupsTool.addGroup('group2', [], [], title="Group 2")
        groupsTool.addGroup('group3', [], [], title="Group 3 accentué")

    def generateUsers(self, portal):
        members = [
            {'username': 'DIispfuF', 'fullname': 'Kevin Hughes', 'email': 'DIispfuF@example.com'},
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
            {'username': 'NP4FMIb5', 'email': 'NP4FMIb5@example.com'}
        ]
        rtool = getToolByName(portal, 'portal_registration')
        for member in members:
            rtool.addMember(member['username'], 'somepassword', properties=member)

PLONE_APP_CONTROLPANEL_FIXTURE = PloneAppControlpanel()
PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_CONTROLPANEL_FIXTURE,),
    name="PloneAppControlpanel:Integration")
PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_CONTROLPANEL_FIXTURE,),
    name="PloneAppControlpanel:Functional")
