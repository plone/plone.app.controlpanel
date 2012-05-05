from zope.site.hooks import getSite
from zope.component import getAdapter
from Products.CMFPlone.PropertiesTool import SimpleItemWithProperties
from plone.app.controlpanel.interfaces import IEditingSchema


def _setProperty(self, id, value, type='string'):
    super(SimpleItemWithProperties, self)._setProperty(id, value, type=type)
    portal = getSite()
    if id in IEditingSchema.names():
        settings = getAdapter(portal, IEditingSchema)
        if value == '':
            value = False
        if id == 'default_editor' and value == False:
            value = 'None'
        setattr(settings, id, value)
