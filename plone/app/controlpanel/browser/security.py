import logging
from Acquisition import aq_inner
from collections import defaultdict
from zope.cachedescriptors.property import Lazy
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.PlonePAS.interfaces.plugins import IUserManagement
from plone.app.controlpanel import _
from plone.app.registry.browser import controlpanel

from plone.app.controlpanel.interfaces import ISecuritySchema

logger = logging.getLogger('plone.app.controlpanel')


class SecurityControlPanelForm(controlpanel.RegistryEditForm):

    id = "SecurityControlPanel"
    label = _(u"Security settings")
    schema = ISecuritySchema


class SecurityControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SecurityControlPanelForm


class EmailLogin(BrowserView):
    """View to help in migrating to or from using email as login.
    """

    duplicates = []
    switched_to_email = 0
    switched_to_userid = 0

    def __call__(self):
        if self.request.form.get('check'):
            self.duplicates = self.check_duplicates()
        if self.request.form.get('switch_to_email'):
            self.switched_to_email = self.switch_to_email()
        if self.request.form.get('switch_to_userid'):
            self.switched_to_userid = self.switch_to_userid()
        return self.index()

    @property
    def _email_list(self):
        context = aq_inner(self.context)
        pas = getToolByName(context, 'acl_users')
        emails = defaultdict(list)
        for user in pas.getUsers():
            if user is None:
                # Created in the ZMI?
                continue
            email = user.getProperty('email', '')
            if email:
                emails[email].append(user.getUserId())
            else:
                logger.warn("User %s has no email address.", user.getUserId())
        return emails

    @Lazy
    def _plugins(self):
        """Give list of proper IUserManagement plugins that can update a user.
        """
        context = aq_inner(self.context)
        pas = getToolByName(context, 'acl_users')
        plugins = []
        for plugin_id, plugin in pas.plugins.listPlugins(IUserManagement):
            if hasattr(plugin, 'updateUser'):
                plugins.append(plugin)
        if not plugins:
            logger.warn("No proper IUserManagement plugins found.")
        return plugins

    def _update_login(self, userid, login):
        """Update login name of user.
        """
        for plugin in self._plugins:
            try:
                plugin.updateUser(userid, login)
            except KeyError:
                continue
            else:
                logger.info("Gave user id %s login name %s",
                            userid, login)
                return 1
        return 0

    def check_duplicates(self):
        duplicates = []
        for email, userids in self._email_list.items():
            if len(userids) > 1:
                logger.warn("Duplicate accounts for email address %s: %r",
                            email, userids)
                duplicates.append((email, userids))

        return duplicates

    def switch_to_email(self):
        if not self._plugins:
            return 0
        success = 0
        for email, userids in self._email_list.items():
            if len(userids) > 1:
                logger.warn("Not setting login name for accounts with same "
                            "email address %s: %r", email, userids)
                continue
            for userid in userids:
                success += self._update_login(userid, email)
        return success

    def switch_to_userid(self):
        context = aq_inner(self.context)
        pas = getToolByName(context, 'acl_users')
        if not self._plugins:
            return 0
        success = 0
        for user in pas.getUsers():
            if user is None:
                # Created in the ZMI?
                continue
            userid = user.getUserId()
            success += self._update_login(userid, userid)
        return success
