# Control panels for Plone 5 have been moved to CMFPlone. We keep those imports
# for backwards compatibility.
from Products.CMFPlone.interfaces import ISearchSchema  # noqa
from Products.CMFPlone.controlpanel.search import SearchControlPanel  # noqa
from Products.CMFPlone.controlpanel.bbb.search import SearchControlPanelAdapter  # noqa
