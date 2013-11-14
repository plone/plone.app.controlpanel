from AccessControl import getSecurityManager
from Acquisition import aq_base
from Acquisition import aq_inner
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.controlpanel.form import ControlPanelView
from plone.memoize.instance import memoize
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility

try:
    from plone.app.event.interfaces import IEventSettings
    HAS_PAE = True
except ImportError:
    HAS_PAE = False


class OverviewControlPanel(ControlPanelView):

    template = ViewPageTemplateFile('overview.pt')

    base_category = 'controlpanel'
    ignored_categories = ('controlpanel_user')

    def __call__(self):
        self.request.set('disable_border', 1)
        return self.template()

    @memoize
    def cptool(self):
        return getToolByName(aq_inner(self.context), 'portal_controlpanel')

    @memoize
    def migration(self):
        return getToolByName(aq_inner(self.context), 'portal_migration')

    @memoize
    def core_versions(self):
        return self.migration().coreVersions()

    def pil(self):
        return 'PIL' in self.core_versions()

    def version_overview(self):

        core_versions = self.core_versions()
        versions = [
            'Plone %s (%s)' % (core_versions['Plone'],
                               core_versions['Plone Instance'])]

        for v in ('CMF', 'Zope', 'Python'):
            versions.append(v + ' ' + core_versions.get(v))
        pil = core_versions.get('PIL', None)
        if pil is not None:
            versions.append('PIL ' + pil)
        return versions

    @memoize
    def is_dev_mode(self):
        qi = getToolByName(aq_inner(self.context), 'portal_quickinstaller')
        return qi.isDevelopmentMode()

    def upgrade_warning(self):
        mt = getToolByName(aq_inner(self.context), 'portal_migration')
        if mt.needUpgrading():
            # if the user can't run the upgrade, no sense in displaying the message
            sm = getSecurityManager()
            if sm.checkPermission(ManagePortal, self.context):
                return True
        return False

    def mailhost_warning(self):
        mailhost = getToolByName(aq_inner(self.context), 'MailHost', None)
        if mailhost is None:
            return True
        mailhost = getattr(aq_base(mailhost), 'smtp_host', None)
        email = getattr(aq_inner(self.context), 'email_from_address', None)
        if mailhost and email:
            return False
        return True

    def timezone_warning(self):
        if not HAS_PAE:
            return False
        portal_timezone = None
        reg = queryUtility(IRegistry, context=self.context, default=None)
        if reg:
            portal_timezone = reg.forInterface(
                IEventSettings,
                prefix="plone.app.event",
                check=False  # Don't fail, if portal_timezone isn't set.
            ).portal_timezone
        if portal_timezone:
            return False
        return True

    def categories(self):
        return self.cptool().getGroups()

    def sublists(self, category):
        return self.cptool().enumConfiglets(group=category)
