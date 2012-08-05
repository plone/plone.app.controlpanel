from zope.site.hooks import getSite
from Products.CMFCore.ActionInformation import Action
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import adapts
from zope.interface import implements
from plone.app.controlpanel.interfaces import ISecuritySchema
from Products.CMFPlone.utils import safe_hasattr
from plone.app.controlpanel import _
from Products.CMFCore.utils import getToolByName


class SecurityControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(ISecuritySchema)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        pprop = getToolByName(self.portal, 'portal_properties')
        self.pmembership = getToolByName(context, 'portal_membership')
        portal_url = getToolByName(context, 'portal_url')
        self.portal = portal_url.getPortalObject()
        self.context = pprop.site_properties

    def get_enable_self_reg(self):
        app_perms = self.portal.rolesOfPermission(
            permission='Add portal member')
        for appperm in app_perms:
            if appperm['name'] == 'Anonymous' \
            and appperm['selected'] == 'SELECTED':
                return True
        return False

    def set_enable_self_reg(self, value):
        app_perms = self.portal.rolesOfPermission(
            permission='Add portal member')
        reg_roles = []
        for appperm in app_perms:
            if appperm['selected'] == 'SELECTED':
                reg_roles.append(appperm['name'])
        if value is True and 'Anonymous' not in reg_roles:
            reg_roles.append('Anonymous')
        if value is False and 'Anonymous' in reg_roles:
            reg_roles.remove('Anonymous')

        self.portal.manage_permission('Add portal member', roles=reg_roles,
                                      acquire=0)

    enable_self_reg = property(get_enable_self_reg, set_enable_self_reg)

    def get_enable_user_pwd_choice(self):
        if self.portal.validate_email:
            return False
        else:
            return True

    def set_enable_user_pwd_choice(self, value):
        if value == True:
            self.portal.validate_email = False
        else:
            self.portal.validate_email = True

    enable_user_pwd_choice = property(get_enable_user_pwd_choice,
                                      set_enable_user_pwd_choice)

    def get_enable_user_folders(self):
        return self.pmembership.getMemberareaCreationFlag()

    def set_enable_user_folders(self, value):
        self.pmembership.memberareaCreationFlag = value
        # support the 'my folder' user action #8417
        portal_actions = getToolByName(self.portal, 'portal_actions', None)
        if portal_actions is not None:
            object_category = getattr(portal_actions, 'user', None)
            if value and not safe_hasattr(object_category, 'mystuff'):
                # add action
                self.add_mystuff_action(object_category)
            elif safe_hasattr(object_category, 'mystuff'):
                a = getattr(object_category, 'mystuff')
                a.visible = bool(value)    # show/hide action

    enable_user_folders = property(get_enable_user_folders,
                                   set_enable_user_folders)

    def add_mystuff_action(self, object_category):
        new_action = Action(
            'mystuff',
            title=_(u'My Folder'),
            description='',
            url_expr='string:${portal/portal_membership/getHomeUrl}',
            available_expr='python:(member is not None) and \
                            (portal.portal_membership.getHomeFolder() is not None) ',
            permissions=('View',),
            visible=True,
            i18n_domain='plone')
        object_category._setObject('mystuff', new_action)
        # move action to top, at least before the logout action
        object_category.moveObjectsToTop(('mystuff'))

    def get_allow_anon_views_about(self):
        return self.context.site_properties.allowAnonymousViewAbout

    def set_allow_anon_views_about(self, value):
        self.context.site_properties.allowAnonymousViewAbout = value

    allow_anon_views_about = property(get_allow_anon_views_about,
                                      set_allow_anon_views_about)

    def get_use_email_as_login(self):
        return self.context.use_email_as_login

    def set_use_email_as_login(self, value):
        if value:
            self.context.manage_changeProperties(use_email_as_login=True)
        else:
            self.context.manage_changeProperties(use_email_as_login=False)

    use_email_as_login = property(get_use_email_as_login,
                                  set_use_email_as_login)


def updateSecuritySettings(settings, event):
    """Update Plone's security settings when the security settings in the
    security control panel changes.
    """
    portal = getSite()
    portal.validate_email = not settings.enable_user_pwd_choice
    portal_properties = getToolByName(portal, "portal_properties")
    site_properties = portal_properties.site_properties
    site_properties.allowAnonymousViewAbout = settings.allow_anon_views_about
    site_properties.use_email_as_login = settings.use_email_as_login
    mtool = getToolByName(portal, "portal_membership")
    mtool.memberareaCreationFlag = settings.enable_user_folders
