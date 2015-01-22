import doctest
from unittest import TestSuite

from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Testing.ZopeTestCase import FunctionalDocFileSuite

from plone.app.controlpanel.tests.cptc import ControlPanelTestCase

setupPloneSite()

OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    tests = [
        # 'editing.txt',
        'filter.txt',
        # 'mail.txt',
        # 'security_enable_user_folder.txt',
        # 'site.txt',
        # 'skins.txt',
        # 'navigation.txt',
        # 'types.txt',
        'syndication.txt'
    ]
    suite = TestSuite()

    for test in tests:
        suite.addTest(FunctionalDocFileSuite(
            test,
            optionflags=OPTIONFLAGS,
            package="plone.app.controlpanel.tests",
            test_class=ControlPanelTestCase))

#    suite.addTest(FunctionalDocFileSuite(
#        'usergroups.txt',
#        optionflags=OPTIONFLAGS,
#        package="plone.app.controlpanel.tests",
#        test_class=UserGroupsControlPanelTestCase))

#    suite.addTest(FunctionalDocFileSuite(
#        'security.txt',
#        optionflags=OPTIONFLAGS,
#        package="plone.app.controlpanel.tests",
#        test_class=EmailLoginSecurityControlPanelTestCase))

    return suite
