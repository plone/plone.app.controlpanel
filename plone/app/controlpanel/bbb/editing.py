from zope.component import adapts
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from zope.interface import implements
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.interfaces import IEditingSchema


class EditingControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(IEditingSchema)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = pprop.site_properties
        self.encoding = pprop.site_properties.default_charset

    visible_ids = ProxyFieldProperty(IEditingSchema['visible_ids'])
    enable_inline_editing = ProxyFieldProperty(
        IEditingSchema['enable_inline_editing'])
    enable_link_integrity_checks = ProxyFieldProperty(
        IEditingSchema['enable_link_integrity_checks'])
    ext_editor = ProxyFieldProperty(
        IEditingSchema['ext_editor'])
    default_editor = ProxyFieldProperty(
        IEditingSchema['default_editor'])
    lock_on_ttw_edit = ProxyFieldProperty(
        IEditingSchema['lock_on_ttw_edit'])


def syncPloneAppRegistryToEditingSiteProperties(settings, event):
    portal = getSite()
    portal_properties = getToolByName(portal, "portal_properties")
    site_properties = portal_properties.site_properties

    if event.record.fieldName == "visible_ids":
        site_properties.visible_ids = settings.visible_ids
        return

    if event.record.fieldName == "enable_inline_editing":
        site_properties.enable_inline_editing = settings.enable_inline_editing
        return

    if event.record.fieldName == "enable_link_integrity_checks":
        site_properties.enable_link_integrity_checks = \
            settings.enable_link_integrity_checks
        return

    if event.record.fieldName == "ext_editor":
        site_properties.ext_editor = settings.ext_editor
        return

    if event.record.fieldName == "default_editor":
        site_properties.default_editor = settings.default_editor
        return

    if event.record.fieldName == "lock_on_ttw_edit":
        site_properties.lock_on_ttw_edit = settings.lock_on_ttw_edit
        return