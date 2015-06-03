# Control panels for Plone 5 have been moved to CMFPlone. We keep those imports
# for backwards compatibility.
from Products.CMFPlone.interfaces import IConfigurationChangedEvent  # noqa
from Products.CMFPlone.controlpanel.events import ConfigurationChangedEvent  # noqa
from Products.CMFPlone.controlpanel.events import handleConfigurationChangedEvent  # noqa
