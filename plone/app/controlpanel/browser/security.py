from logging import getLogger
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import ISecuritySchema

log = getLogger('Plone')


class SecurityControlPanel(controlpanel.RegistryEditForm):

    schema = ISecuritySchema
    label = _(u"Mail settings")
    description = _(u"""""")

    def updateFields(self):
        super(SecurityControlPanel, self).updateFields()

    def updateWidgets(self):
        super(SecurityControlPanel, self).updateWidgets()

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@security-controlpanel")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Changes canceled."),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


class SecurityControlPanelView(controlpanel.ControlPanelFormWrapper):
    form = SecurityControlPanel
