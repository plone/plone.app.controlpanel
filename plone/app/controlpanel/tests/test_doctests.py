import doctest
from unittest import TestSuite

from plone.app.testing import api

from plone.app.controlpanel.tests.cptc import ControlPanelTestCase
from plone.app.controlpanel.tests.cptc import UserGroupsControlPanelTestCase
from plone.app.controlpanel.tests.cptc import EmailLoginSecurityControlPanelTestCase

OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    tests = ['editing.txt',
             'filter.txt',
             'mail.txt',
             'maintenance.txt',
             'security_enable_user_folder.txt',
#             'search.txt',
#             'site.txt',
#             'skins.txt',
             'markup.txt',
             'navigation.txt',
             'types.txt',
             'syndication.txt'
             ]
    suite = TestSuite()

    for test in tests:
        suite.addTest(api.DocFileSuite(
            test,
            optionflags=OPTIONFLAGS,
            package="plone.app.controlpanel.tests",
            test_class=ControlPanelTestCase))
        
    suite.addTest(api.DocFileSuite(
        'usergroups.txt',
        optionflags=OPTIONFLAGS,
        package="plone.app.controlpanel.tests",
        test_class=UserGroupsControlPanelTestCase))

    suite.addTest(FunctionalDocFileSuite(
        'security.txt',
        optionflags=OPTIONFLAGS,
        package="plone.app.controlpanel.tests",
        test_class=EmailLoginSecurityControlPanelTestCase))

    return suite
