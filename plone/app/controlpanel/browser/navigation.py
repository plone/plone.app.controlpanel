from plone.app.vocabularies.types import BAD_TYPES
from logging import getLogger
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import INavigationSchema

log = getLogger('Plone')


class NavigationControlPanel(controlpanel.RegistryEditForm):

    schema = INavigationSchema
    id = "NavigationControlPanel"
    label = _(u"Navigation settings")
    description = _(
        u"Lets you control how navigation is constructed in your site." +
        u"Note that to control how the navigation tree is displayed, you " +
        u"should go to 'Manage portlets' at the root of the site (or " +
        u"wherever a navigation tree portlet has been added) and change " +
        u"its settings directly.")

    def updateFields(self):
        super(NavigationControlPanel, self).updateFields()
        self.fields['displayed_types'].widgetFactory = \
            CheckBoxFieldWidget
        self.fields['workflow_states_to_show'].widgetFactory = \
            CheckBoxFieldWidget

    def updateWidgets(self):
        super(NavigationControlPanel, self).updateWidgets()

    @button.buttonAndHandler(_('Save'), name=None)
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@navigation-controlpanel")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Changes canceled."),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


def updateNavigationSettings(settings, event):
    portal = getSite()
    ttool = getToolByName(portal, 'portal_types')
    pprop = getToolByName(portal, 'portal_properties')
    siteProps = pprop['site_properties']
    navProps = pprop['navtree_properties']

    if event.record.fieldName == "generate_tabs":
        siteProps.disable_folder_sections = not settings.generate_tabs
        return

    if event.record.fieldName == "nonfolderish_tabs":
        siteProps.disable_nonfolderish_sections = \
            not settings.nonfolderish_tabs
        return

    if event.record.fieldName == "displayed_types":
        allTypes = ttool.listContentTypes()
        blacklistedTypes = [
            t for t in allTypes \
            if t not in settings.displayed_types \
            or t in BAD_TYPES]
        navProps.metaTypesNotToList = blacklistedTypes
        return

    if event.record.fieldName == "filter_on_workflow":
        navProps.enable_wf_state_filtering = settings.filter_on_workflow
        return
    if event.record.fieldName == "workflow_states_to_show":
        navProps.wf_states_to_show = settings.workflow_states_to_show
        return

    if event.record.fieldName == "show_excluded_items":
        navProps.showAllParents = settings.show_excluded_items


class NavigationControlPanelView(controlpanel.ControlPanelFormWrapper):
    form = NavigationControlPanel
