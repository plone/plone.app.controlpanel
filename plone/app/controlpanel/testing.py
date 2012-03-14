from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
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

PLONE_APP_CONTROLPANEL_FIXTURE = PloneAppControlpanel()
PLONE_APP_CONTROLPANEL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_CONTROLPANEL_FIXTURE,),
    name="PloneAppControlpanel:Integration")
PLONE_APP_CONTROLPANEL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_CONTROLPANEL_FIXTURE,),
    name="PloneAppControlpanel:Functional")
