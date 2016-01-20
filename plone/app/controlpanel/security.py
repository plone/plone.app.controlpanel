# Control panels for Plone 5 have been moved to CMFPlone. We keep those imports
# for backwards compatibility.
from Products.CMFPlone.interfaces import ISecuritySchema  # noqa
from Products.CMFPlone.controlpanel.browser.security import SecurityControlPanel  # noqa
from Products.CMFPlone.controlpanel.bbb.security import SecurityControlPanelAdapter  # noqa
