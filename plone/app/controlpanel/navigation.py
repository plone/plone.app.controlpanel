# Control panels for Plone 5 have been moved to CMFPlone. We keep those imports
# for backwards compatibility.
from Products.CMFPlone.interfaces import INavigationSchema  # noqa
from Products.CMFPlone.controlpanel.navigation import NavigationControlPanel  # noqa
from Products.CMFPlone.controlpanel.bbb.navigation import NavigationControlPanelAdapter  # noqa
