from zope.component import adapts
from zope.interface import implements
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form
from plone.z3cform import layout
from Products.CMFPlone import PloneMessageFactory as _
from plone.autoform.form import AutoExtensibleForm

from plone.app.controlpanel.interfaces import IEditingSchema


class EditingControlPanel(AutoExtensibleForm, form.EditForm):
    schema = IEditingSchema
    id = "editing-control-panel"
    label = _("Editing settings")
    description = _("General editing settings.")
    form_name = _("Editing settings")
    control_panel_view = "editing-controlpanel"

    def getContent(self):
        portal = getSite()
        pprop = getToolByName(portal, 'portal_properties')
        site_properties = pprop.site_properties
        self.context = site_properties
        context = dict()
        context['visible_ids'] = site_properties.getProperty('visible_ids')
        context['enable_inline_editing'] = \
            site_properties.getProperty('enable_inline_editing')
        context['enable_link_integrity_checks'] = \
            site_properties.getProperty('enable_link_integrity_checks')
        context['ext_editor'] = site_properties.getProperty('ext_editor')
        context['default_editor'] = site_properties.getProperty(
            'default_editor')
        context['lock_on_ttw_edit'] = site_properties.getProperty(
            'lock_on_ttw_edit')
        return context

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        portal = getSite()
        pprop = getToolByName(portal, 'portal_properties')
        site_properties = pprop.site_properties
        site_properties.manage_changeProperties(
            visible_ids=data['visible_ids'],
            enable_inline_editing=data['enable_inline_editing'],
            enable_link_integrity_checks=data['enable_link_integrity_checks'],
            ext_editor=data['ext_editor'],
            default_editor=data['default_editor'],
            lock_on_ttw_edit=data['lock_on_ttw_edit'])
        #IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
        #S                                              "info")
        self.request.response.redirect("@@editing-controlpanel")

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes canceled."), "info")
        self.request.response.redirect("plone_control_panel")


class ControlPanelFormWrapper(layout.FormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
    panel layout.
    """

    index = ViewPageTemplateFile('controlpanel_layout.pt')


EditingControlPanelView = layout.wrap_form(
    EditingControlPanel, ControlPanelFormWrapper)
