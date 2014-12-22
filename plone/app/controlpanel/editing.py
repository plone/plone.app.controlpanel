# Control panels for Plone 5 have been moved to CMFPlone. We keep those imports
# for backwards compatibility.
from Products.CMFPlone.interfaces import IEditingSchema  # noqa
from Products.CMFPlone.controlpanel.editing import EditingControlPanel  # noqa
from Products.CMFPlone.controlpanel.bbb.editing import EditingControlPanelAdapter  # noqa
