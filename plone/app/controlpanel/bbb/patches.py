from zope.site.hooks import getSite
from zope.component import getAdapter
from Products.CMFPlone.PropertiesTool import SimpleItemWithProperties
from plone.app.controlpanel.interfaces import IEditingSchema
from plone.app.controlpanel.interfaces import ISecuritySchema


def _setProperty(self, id, value, type='string'):
    """Use OFS.PropertyManager _setProperty method to set a property
    """
    super(SimpleItemWithProperties, self)._setProperty(id, value, type=type)
    portal = getSite()
    if id in IEditingSchema.names():
        settings = getAdapter(portal, IEditingSchema)
        if value == '':
            value = False
        if id == 'default_editor' and value == False:
            value = 'None'
        setattr(settings, id, value)


def _updateProperty(self, id, value):
    super(SimpleItemWithProperties, self)._updateProperty(id, value)
    #print "_updateProperty(): %s | %s" % (id, value)
