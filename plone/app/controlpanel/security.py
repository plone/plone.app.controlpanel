import logging
from collections import defaultdict
from zope.interface import Interface
from zope.component import adapts
from zope.formlib.form import FormFields
from zope.interface import implements
from zope.schema import Bool
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.ActionInformation import Action
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.utils import safe_hasattr
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five import BrowserView

from form import ControlPanelForm

logger = logging.getLogger('plone.app.controlpanel')


class ISecuritySchema(Interface):

    enable_self_reg = Bool(
        title=_(u'Enable self-registration'),
        description=_(u"Allows users to register themselves on the site. If "
                      "not selected, only site managers can add new users."),
        default=False,
        required=False)

    enable_user_pwd_choice = Bool(
        title=_(u'Let users select their own passwords'),
        description=_(u"If not selected, a URL will be generated and "
                      "e-mailed. Users are instructed to follow the link to "
                      "reach a page where they can change their password and "
                      "complete the registration process; this also verifies "
                      "that they have entered a valid email address."),
        default=False,
        required=False)

    enable_user_folders = Bool(
        title=_(u'Enable User Folders'),
        description=_(u"If selected, home folders where users can create "
                      "content will be created when they log in."),
        default=False,
        required=False)

    allow_anon_views_about = Bool(
        title=_(u"Allow anyone to view 'about' information"),
        description=_(u"If not selected only logged-in users will be able to "
                      "view information about who created an item and when it "
                      "was modified."),
        default=False,
        required=False)

    use_email_as_login = Bool(
        title=_(u'Use email address as login name'),
        description = _(
            u"Allows users to login with their email address instead "
            u"of specifying a separate login name. This also updates "
            u"the login name of existing users, which may take a "
            u"while on large sites. The login name is saved as "
            u"lower case, but to be userfriendly it does not matter "
            u"which case you use to login. When duplicates are found, "
            u"saving this form will fail. You can use the "
            u"@@migrate-to-emaillogin page to show the duplicates."),
        default=False,
        required=False)

    use_uuid_as_userid = Bool(
        title=_(u'Use UUID user ids'),
        description = _(
            u"Use automatically generated UUIDs as user id for new users. "
            u"When not turned on, the default is to use the same as the "
            u"login name, or when using the email address as login name we "
            u"generate a user id based on the fullname."),
        default=False,
        required=False)


class SecurityControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ISecuritySchema)

    def __init__(self, context):
        super(SecurityControlPanelAdapter, self).__init__(context)
        pprop = getToolByName(context, 'portal_properties')
        self.pmembership = getToolByName(context, 'portal_membership')
        portal_url = getToolByName(context, 'portal_url')
        self.portal = portal_url.getPortalObject()
        self.context = pprop.site_properties

    def get_enable_self_reg(self):
        app_perms = self.portal.rolesOfPermission(permission='Add portal member')
        for appperm in app_perms:
            if appperm['name'] == 'Anonymous' and \
               appperm['selected'] == 'SELECTED':
                return True
        return False

    def set_enable_self_reg(self, value):
        app_perms = self.portal.rolesOfPermission(permission='Add portal member')
        reg_roles = []
        for appperm in app_perms:
            if appperm['selected'] == 'SELECTED':
                reg_roles.append(appperm['name'])
        if value == True and 'Anonymous' not in reg_roles:
            reg_roles.append('Anonymous')
        if value == False and 'Anonymous' in reg_roles:
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
        return self.context.allowAnonymousViewAbout

    def set_allow_anon_views_about(self, value):
        self.context.allowAnonymousViewAbout = value

    allow_anon_views_about = property(get_allow_anon_views_about,
                                      set_allow_anon_views_about)

    def get_use_email_as_login(self):
        return self.context.getProperty('use_email_as_login')

    def set_use_email_as_login(self, value):
        context = aq_inner(self.context)
        if context.getProperty('use_email_as_login') == value:
            # no change
            return
        if value:
            migrate_to_email_login(self.context)
        else:
            migrate_from_email_login(self.context)

    use_email_as_login = property(get_use_email_as_login,
                                  set_use_email_as_login)

    def get_use_uuid_as_userid(self):
        return self.context.getProperty('use_uuid_as_userid')

    def set_use_uuid_as_userid(self, value):
        self.context.manage_changeProperties(use_uuid_as_userid=value)

    use_uuid_as_userid = property(get_use_uuid_as_userid,
                                  set_use_uuid_as_userid)


def migrate_to_email_login(context):
    # Note that context could be the Plone Site or site_properties.
    pas = getToolByName(context, 'acl_users')
    pprop = getToolByName(context, 'portal_properties')
    site_props = pprop.site_properties
    site_props.manage_changeProperties(use_email_as_login=True)

    # We want the login name to be lowercase here.  This is new in
    # PAS.  Using 'manage_changeProperties' would change the login
    # names immediately, but we want to do that explicitly ourselves
    # and set the lowercase email address as login name, instead of
    # the lower case user id.
    #pas.manage_changeProperties(login_transform='lower')
    pas.login_transform = 'lower'

    # Update the users.
    for user in pas.getUsers():
        if user is None:
            continue
        user_id = user.getUserId()
        email = user.getProperty('email', '')
        if email:
            login_name = pas.applyTransform(email)
            pas.updateLoginName(user_id, login_name)
        else:
            logger.warn("User %s has no email address.", user_id)


def migrate_from_email_login(context):
    # Note that context could be the Plone Site or site_properties.
    pas = getToolByName(context, 'acl_users')
    pprop = getToolByName(context, 'portal_properties')
    site_props = pprop.site_properties
    site_props.manage_changeProperties(use_email_as_login=False)
    # Whether the login name is lowercase or not does not really
    # matter for this use case, but it may be better not to change
    # it at this point.

    # We do want to update the users.
    for user in pas.getUsers():
        if user is None:
            continue
        user_id = user.getUserId()
        # If we keep the transform to lowercase, then we must apply it
        # here as well, otherwise some users will not be able to
        # login, as their user id may be mixed or upper case.
        login_name = pas.applyTransform(user_id)
        pas.updateLoginName(user_id, login_name)


class SecurityControlPanel(ControlPanelForm):

    form_fields = FormFields(ISecuritySchema)

    label = _("Security settings")
    description = _("Security settings for this site.")
    form_name = _("Security settings")


class EmailLogin(BrowserView):
    """View to help in migrating to or from using email as login.

    We used to change the login name of existing users here, but that
    is now done by checking or unchecking the option in the security
    control panel.  Here you can only search for duplicates.
    """

    duplicates = []

    def __call__(self):
        if self.request.form.get('check_email'):
            self.duplicates = self.check_email()
        elif self.request.form.get('check_userid'):
            self.duplicates = self.check_userid()
        return self.index()

    @property
    def _email_list(self):
        context = aq_inner(self.context)
        pas = getToolByName(context, 'acl_users')
        emails = defaultdict(list)
        orig_transform = pas.login_transform
        try:
            if not orig_transform:
                # Temporarily set this to lower, as that will happen
                # when turning emaillogin on.
                pas.login_transform = 'lower'
            for user in pas.getUsers():
                if user is None:
                    # Created in the ZMI?
                    continue
                email = user.getProperty('email', '')
                if email:
                    email = pas.applyTransform(email)
                else:
                    logger.warn("User %s has no email address.",
                                user.getUserId())
                    # Add the normal login name anyway.
                    email = pas.applyTransform(user.getUserName())
                emails[email].append(user.getUserId())
        finally:
            pas.login_transform = orig_transform
            return emails

    def check_email(self):
        duplicates = []
        for email, userids in self._email_list.items():
            if len(userids) > 1:
                logger.warn("Duplicate accounts for email address %s: %r",
                            email, userids)
                duplicates.append((email, userids))

        return duplicates

    @property
    def _userid_list(self):
        # user ids are unique, but their lowercase version might not
        # be unique.
        context = aq_inner(self.context)
        pas = getToolByName(context, 'acl_users')
        userids = defaultdict(list)
        orig_transform = pas.login_transform
        try:
            if not orig_transform:
                # Temporarily set this to lower, as that will happen
                # when turning emaillogin on.
                pas.login_transform = 'lower'
            for user in pas.getUsers():
                if user is None:
                    continue
                login_name = pas.applyTransform(user.getUserName())
                userids[login_name].append(user.getUserId())
        finally:
            pas.login_transform = orig_transform
            return userids

    def check_userid(self):
        duplicates = []
        for login_name, userids in self._userid_list.items():
            if len(userids) > 1:
                logger.warn("Duplicate accounts for lower case user id "
                            "%s: %r", login_name, userids)
                duplicates.append((login_name, userids))

        return duplicates

    def switch_to_email(self):
        # This is not used and is only here for backwards
        # compatibility.  It avoids a test failure in
        # Products.CMFPlone.
        migrate_to_email_login(self.context)

    def switch_to_userid(self):
        # This is not used and is only here for backwards
        # compatibility.  It avoids a test failure in
        # Products.CMFPlone.
        migrate_from_email_login(self.context)
