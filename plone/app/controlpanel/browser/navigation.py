from plone.app.vocabularies.types import BAD_TYPES
from logging import getLogger
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName

from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import INavigationSchema

log = getLogger('Plone')


class NavigationControlPanelForm(controlpanel.RegistryEditForm):

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
        super(NavigationControlPanelForm, self).updateFields()
        self.fields['displayed_types'].widgetFactory = \
            CheckBoxFieldWidget
        self.fields['workflow_states_to_show'].widgetFactory = \
            CheckBoxFieldWidget


class NavigationControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NavigationControlPanelForm


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
