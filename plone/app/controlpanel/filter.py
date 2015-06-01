# Control panels for Plone 5 have been moved to CMFPlone. We keep those imports
# for backwards compatibility.
from Products.CMFPlone.interfaces import IFilterTagsSchema  # noqa
from Products.CMFPlone.interfaces import IFilterAttributesSchema  # noqa
from Products.CMFPlone.interfaces import IFilterEditorSchema  # noqa
from Products.CMFPlone.controlpanel.filter import FilterControlPanel  # noqa
from Products.CMFPlone.controlpanel.bbb.filter import FilterControlPanelAdapter  # noqa
