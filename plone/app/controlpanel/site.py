# Control panels for Plone 5 have been moved to CMFPlone. We keep those imports
# for backwards compatibility.
from Products.CMFPlone.interfaces import ISiteSchema  # noqa
from Products.CMFPlone.controlpanel.site import SiteControlPanel  # noqa
from Products.CMFPlone.controlpanel.bbb.site import SiteControlPanelAdapter  # noqa
