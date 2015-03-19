import doctest
from unittest import TestSuite

from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Testing.ZopeTestCase import FunctionalDocFileSuite

from plone.app.controlpanel.tests.cptc import ControlPanelTestCase

setupPloneSite()

OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


def test_suite():
    tests = [
        'filter.txt',
    ]
    suite = TestSuite()

    for test in tests:
        suite.addTest(FunctionalDocFileSuite(
            test,
            optionflags=OPTIONFLAGS,
            package="plone.app.controlpanel.tests",
            test_class=ControlPanelTestCase))

    return suite
