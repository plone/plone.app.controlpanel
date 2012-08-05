from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from logging import getLogger
from z3c.form import button

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import IEditingSchema

log = getLogger('Plone')


class EditingControlPanelForm(controlpanel.RegistryEditForm):

    id = "EditingControlPanel"
    label = _(u"Editing settings")
    schema = IEditingSchema

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        super(EditingControlPanelForm, self).handleSave(self, action)

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        super(EditingControlPanelForm, self).handleCancel(self, action)


class EditingControlPanel(controlpanel.ControlPanelFormWrapper):
    form = EditingControlPanelForm


def updateEditingSettings(settings, event):
    """Update Plone's editing settings when the editing settings in the
    editing control panel change.
    """
    portal = getSite()
    portal_properties = getToolByName(portal, "portal_properties")
    site_properties = portal_properties.site_properties
    site_properties.visible_ids = settings.visible_ids
    site_properties.enable_inline_editing = settings.enable_inline_editing
    site_properties.enable_link_integrity_checks = \
        settings.enable_link_integrity_checks
    site_properties.ext_editor = settings.ext_editor
    site_properties.default_editor = settings.default_editor
    site_properties.lock_on_ttw_edit = settings.lock_on_ttw_edit
