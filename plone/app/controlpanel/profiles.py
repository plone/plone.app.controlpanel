from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        """
        Prevents uninstall profile from showing up in the profile list
        when creating a Plone site.
        """
        return [
            u'plone.app.controlpanel:uninstall',
            u'plone.app.controlpanel:default'
        ]