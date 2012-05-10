from zope.component import queryUtility

from plone.registry.interfaces import IRegistry

from Products.CMFPlone.PropertiesTool import SimpleItemWithProperties
from plone.app.controlpanel.interfaces import IMailSchema


def _updateProperty(self, id, value):
    super(SimpleItemWithProperties, self)._updateProperty(id, value)
    registry = queryUtility(IRegistry, context=self)
    if registry:
        if id in IMailSchema.names():
            settings = registry.forInterface(IMailSchema)
            setattr(settings, id, value)
