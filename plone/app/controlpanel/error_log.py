# -*- coding: utf-8 -*-
from DateTime import DateTime
from zope.publisher.browser import BrowserView

from Products.CMFPlone import PloneMessageFactory as _


class ErrorLogSetProperties(BrowserView):

    def __call__(self):
        error_log = self.context.error_log
        putils = self.context.plone_utils

        keep_entries = self.request['keep_entries']
        copy_to_zlog = self.request['copy_to_zlog']
        ignored_exceptions = self.request['ignored_exceptions']

        error_log.setProperties(keep_entries,
                                copy_to_zlog,
                                ignored_exceptions)

        putils.addPortalMessage(_(u'Changes made.'))

        url = self.context.absolute_url() + '/prefs_error_log_form'
        return self.request.response.redirect(url)


class ErrorLogUpdate(BrowserView):

    def __call__(self):
        error_log = self.context.error_log
        putils = self.context.plone_utils

        membership_tool = self.context.portal_membership
        member = membership_tool.getAuthenticatedMember()

        if getattr(self.request, 'form.button.search', None) is not None:
            search = self.request.form.get('search_entry')
            if search == '':
                member.setProperties(error_log_update=0.0)
                putils.addPortalMessage(_(u'Showing all entries'))
            else:
                url = self.context.absolute_url()
                url += '/prefs_error_log_showEntry?id=%s' % search
                return self.request.response.redirect(url)
        elif getattr(self.request, 'form.button.showall', None) is not None:
            member.setProperties(error_log_update=0.0)
            putils.addPortalMessage(_(u'Showing all entries'))
        elif getattr(self.request, 'form.button.clear', None) is not None:
            member.setProperties(error_log_update=DateTime().timeTime())
            putils.addPortalMessage(_(u'Entries cleared'))

        url = self.context.absolute_url() + '/prefs_error_log_form'
        return self.request.response.redirect(url)
