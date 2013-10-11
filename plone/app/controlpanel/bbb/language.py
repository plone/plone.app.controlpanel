from Acquisition import aq_inner
from Products.statusmessages.interfaces import IStatusMessage

from zope.site.hooks import getSite
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import adapts
from zope.component import getAdapter
from zope.interface import implements
from plone.app.controlpanel.interfaces import ILanguageSchema
from plone.app.controlpanel import _
from Products.CMFCore.utils import getToolByName


class LanguageControlPanelAdapter(object):

    adapts(IPloneSiteRoot)
    implements(ILanguageSchema)

    def __init__(self, context):
        self.context = context
        self.portal = getSite()
        self.context = getToolByName(self.portal, 'portal_languages')

    def get_default_language(self):
        return aq_inner(self.context).getDefaultLanguage()

    def set_default_language(self, value):
        context = aq_inner(self.context)
        if isinstance(value, tuple):
            value = value[0]
        supported_langs = context.getSupportedLanguages()
        if value not in supported_langs:
            context.supported_langs = [value]
        context.setDefaultLanguage(value)

    default_language = property(get_default_language,
                                set_default_language)

    def get_use_combined_language_codes(self):
        return aq_inner(self.context).use_combined_language_codes

    def set_use_combined_language_codes(self, value):
        context = aq_inner(self.context)
        # We are disabling the combined codes, but still have one selected
        # as the default.
        default = context.getDefaultLanguage()
        if len(default.split('-')) > 1:
            # XXX This should be done in some kind of validate method instead,
            # but I have no time to figure out that part of formlib right now
            request = context.REQUEST
            message = _(u"You cannot disable country-specific language "
                        u"variants, please choose a different site "
                        u"language first.")
            IStatusMessage(request).addStatusMessage(message, type='error')
        else:
            context.use_combined_language_codes = value

    use_combined_language_codes = property(get_use_combined_language_codes,
                                           set_use_combined_language_codes)
