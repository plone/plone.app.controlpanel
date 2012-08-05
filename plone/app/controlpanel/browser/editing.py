from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from logging import getLogger
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import IEditingSchema

log = getLogger('Plone')


class EditingControlPanelForm(controlpanel.RegistryEditForm):

    schema = IEditingSchema
    id = "EditingControlPanel"
    label = _(u"Editing settings")
    description = _(u"""""")

    def updateFields(self):
        super(EditingControlPanelForm, self).updateFields()

    def updateWidgets(self):
        super(EditingControlPanelForm, self).updateWidgets()

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@editing-controlpanel")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Changes canceled."),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


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


class EditingControlPanel(controlpanel.ControlPanelFormWrapper):
    form = EditingControlPanelForm
