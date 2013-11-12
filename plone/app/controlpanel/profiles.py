from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable


class HiddenProfilesAndProducts(object):
    implements(INonInstallable)
            
    def getNonInstallableProducts(self):
        return ['plone.app.controlpanel']