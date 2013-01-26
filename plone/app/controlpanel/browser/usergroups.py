from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.z3cform import layout
from plone.autoform.form import AutoExtensibleForm
from plone.app.controlpanel import _
from z3c.form import form

from plone.app.controlpanel.interfaces import IUserGroupsSettingsSchema


class UserGroupsSettingsControlPanel(AutoExtensibleForm, form.EditForm):
    schema = IUserGroupsSettingsSchema
    id = "usergroupsettings-control-panel"
    label = _("User/Groups settings")
    description = _("User and groups settings for this site.")
    form_name = _("User/Groups settings")
    control_panel_view = "usergroups-controlpanel"


class ControlPanelFormWrapper(layout.FormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
    panel layout.
    """

    index = ViewPageTemplateFile('controlpanel_usergroups_layout.pt')


UserGroupsSettingsPanelView = layout.wrap_form(
    UserGroupsSettingsControlPanel, ControlPanelFormWrapper
)
