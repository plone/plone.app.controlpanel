from zope.component import adapts
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from zope.interface import implements
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.interfaces import ICalendarSchema


class CalendarControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(ICalendarSchema)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        self.context = getToolByName(self.portal, 'portal_calendar')

    firstweekday = ProxyFieldProperty(ICalendarSchema['firstweekday'])
    calendar_states = ProxyFieldProperty(ICalendarSchema['calendar_states'])
