# Control panels for Plone 5 have been moved to CMFPlone. We keep those imports
# for backwards compatibility.
from Products.CMFPlone.interfaces import ILanguageSelectionSchema  # noqa
from Products.CMFPlone.controlpanel.language import LanguageControlPanel  # noqa
from Products.CMFPlone.controlpanel.bbb.language import LanguageControlPanelAdapter  # noqa
