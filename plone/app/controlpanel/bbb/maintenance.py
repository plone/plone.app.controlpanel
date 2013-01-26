from plone.app.controlpanel.interfaces import IMaintenanceSchema
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.interface import implements
from Products.CMFPlone.interfaces import IPloneSiteRoot


class MaintenanceControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(IMaintenanceSchema)

    def __init__(self, context):
        pprop = getToolByName(context, 'portal_properties')
        self.context = pprop.site_properties

    def get_days(self):
        return self.context.number_of_days_to_keep

    def set_days(self, value):
        if isinstance(value, basestring):
            value = int(value)
        self.context.number_of_days_to_keep = value

    days = property(get_days, set_days)
