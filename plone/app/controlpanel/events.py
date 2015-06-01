from zope.interface import implements

from plone.app.controlpanel.interfaces import IConfigurationChangedEvent


class ConfigurationChangedEvent(object):
    implements(IConfigurationChangedEvent)

    def __init__(self, context, data):
        self.context = context
        self.data = data
