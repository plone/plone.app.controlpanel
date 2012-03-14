from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import form
from plone.z3cform import layout

from zope.interface import Interface
from zope.schema import Bool
from zope.schema import Choice

from Products.CMFPlone import PloneMessageFactory as _

from plone.autoform.form import AutoExtensibleForm


class IEditingSchema(Interface):

    visible_ids = Bool(
        title=_(u"Show 'Short Name' on content?"),
        description=_(u"Display and allow users to edit the "
             "'Short name' content identifiers, which form the "
             "URL part of a content item's address. Once "
             "enabled, users will then be able to enable this "
             "option in their preferences."),
        default=False,
        required=False)

    default_editor = Choice(
        title=_(u'Default editor'),
        description=_(u"Select the default wysiwyg "
            "editor. Users will be able to choose their "
            "own or select to use the site default."),
        default=u'TinyMCE',
        missing_value=set(),
        vocabulary="plone.app.vocabularies.AvailableEditors",
        required=False)

    ext_editor = Bool(
        title=_(u'Enable External Editor feature'),
        description=_(u"Determines if the external editor "
            "feature is enabled. This feature requires a "
            "special client-side application installed. The "
            "users also have to enable this in their "
            "preferences."),
        default=False,
        required=False)

    enable_inline_editing = Bool(
        title=_(u"Enable inline editing"),
        description=_(u"Check this to enable "
                      "inline editing on the site."),
        default=True,
        required=False)

    enable_link_integrity_checks = Bool(
        title=_(u"Enable link integrity checks"),
        description=_(u"Determines if the users should get "
            "warnings when they delete or move content that "
            "is linked from inside the site."),
        default=True,
        required=False)

    lock_on_ttw_edit = Bool(
        title=_(u"Enable locking for through-the-web edits"),
        description=_(u"Disabling locking here will only "
              "affect users editing content through the "
              "Plone web UI.  Content edited via WebDAV "
              "clients will still be subject to locking."),
        default=True,
        required=False)


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
        context['default_editor'] = site_properties.getProperty('default_editor')
        context['lock_on_ttw_edit'] = site_properties.getProperty('lock_on_ttw_edit')
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
