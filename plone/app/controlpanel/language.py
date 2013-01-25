from zope.event import notify
from plone.app.form.widgets import LanguageDropdownChoiceWidget

from zope.formlib.form import FormFields
from zope.formlib import form
from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import List

from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage

from plone.app.controlpanel.events import ConfigurationChangedEvent
from plone.app.controlpanel.form import ControlPanelForm

from plone.protect import CheckAuthenticator


class ILanguageSelectionSchema(Interface):

    use_combined_language_codes = Bool(
        title=_(u'label_allow_combined_language_codes',
                default=u"Show country-specific language variants"),
        description=_(u"help_allow_combined_language_codes",
                      default=u"Examples: pt-br (Brazilian Portuguese), "
                               "en-us (American English) etc."),
        default=False,
        required=False)

    default_language = Choice(
        title=_(u"heading_site_language",
                default=u"Site language"),
        description=_(u"description_site_language",
                      default=u"The language used for the content and the UI "
                               "of this site."),
        required=True,
        vocabulary="plone.app.vocabularies.AvailableContentLanguages")

    available_languages = List(
        title=_(u"heading_available_languages",
                default=u"Available languages"),
        description=_(u"description_available_languages",
                default=u"The languages in which the site should be "
                        u"translatable."),
        required=True,
        missing_value=set(),
        value_type=Choice(
            vocabulary=("plone.app.vocabularies.AvailableContentLanguages")))

    use_content_negotiation = Bool(
        title=_(u"heading_language_of_the_content",
                default=u"Use the language of the content item."),
        description=_(u"description_language_of_the_content",
                default=u"Use the language of the content item."),
        required=False,
        )

    use_path_negotiation = Bool(
        title=_(
            u"heading_language_codes_in_URL",
            default=u"Use language codes in URL path for manual override."),
        description=_(
            u"description_language_codes_in_URL",
            default=u"Use language codes in URL path for manual override."),
        required=False,
        )

    use_cookie_negotiation = Bool(
        title=_(u"heading_cookie_manual_override",
                default=(u"Use cookie for manual override. (Required for "
                         u"the language selector viewlet to be rendered.)")),
        description=_(
            u"description_cookie_manual_override",
            default=(u"Use cookie for manual override. (Required for the "
                     u"language selector viewlet to be rendered.)")),
        required=False,
        )

    authenticated_users_only = Bool(
        title=_(u"heading_auth_cookie_manual_override",
                default=u"Authenticated users only."),
        description=_(
            u"description_auth_ookie_manual_override",
            default=(u"Authenticated users only. Use cookie for manual "
                     u"override. (Required for the language selector viewlet "
                     u"to be rendered.)")),
        required=False,
        )

    set_cookie_everywhere = Bool(
        title=_(
            u"heading_set_language_cookie_always",
            default=(u"Set the language cookie always, i.e. also when the "
                     u"'set_language' request parameter is absent.")),
        description=_(
            u"description_set_language_cookie_always",
            default=(u"Set the language cookie always, i.e. also when the "
                     u"'set_language' request parameter is absent.")),
        required=False,
        )

    use_subdomain_negotiation = Bool(
        title=_(u"heading_use_subdomain",
                default=u"Use subdomain (e.g.: de.plone.org)."),
        description=_(u"description_use_subdomain",
                default=u"Use subdomain (e.g.: de.plone.org)."),
        required=False,
        )

    use_cctld_negotiation = Bool(
        title=_(u"heading_top_level_domain",
                default=u"Use top-level domain (e.g.: www.plone.de)."),
        description=_(u"description_top_level_domain",
                default=u"Use top-level domain (e.g.: www.plone.de)."),
        required=False,
        )

    use_request_negotiation = Bool(
        title=_(u"heading_browser_language_request_negotiation",
                default=u"Use browser language request negotiation."),
        description=_(u"description_browser_language_request_negotiation",
                default=u"Use browser language request negotiation."),
        required=False,
        )


class LanguageControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ILanguageSelectionSchema)

    def __init__(self, context):
        super(LanguageControlPanelAdapter, self).__init__(context)
        self.context = getToolByName(context, 'portal_languages')

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
                         "variants, please choose a different site "
                         "language first.")
            IStatusMessage(request).addStatusMessage(message, type='error')
        else:
            context.use_combined_language_codes = value

    def get_available_languages(self):
        return [unicode(l) for l in self.context.getSupportedLanguages()]

    def set_available_languages(self, value):
        languages = [str(l) for l in value]
        self.context.supported_langs = languages

    def get_use_content_negotiation(self):
        return self.context.use_content_negotiation

    def set_use_content_negotiation(self, value):
        self.context.use_content_negotiation = value

    def get_use_path_negotiation(self):
        return self.context.use_path_negotiation

    def set_use_path_negotiation(self, value):
        self.context.use_path_negotiation = value

    def get_use_cookie_negotiation(self):
        return self.context.use_cookie_negotiation

    def set_use_cookie_negotiation(self, value):
        self.context.use_cookie_negotiation = value

    def get_authenticated_users_only(self):
        return self.context.authenticated_users_only

    def set_authenticated_users_only(self, value):
        self.context.authenticated_users_only = value

    def get_set_cookie_everywhere(self):
        return self.context.set_cookie_everywhere

    def set_set_cookie_everywhere(self, value):
        self.context.set_cookie_everywhere = value

    def get_use_subdomain_negotiation(self):
        return self.context.use_subdomain_negotiation

    def set_use_subdomain_negotiation(self, value):
        self.context.use_subdomain_negotiation = value

    def get_use_cctld_negotiation(self):
        return self.context.use_cctld_negotiation

    def set_use_cctld_negotiation(self, value):
        self.context.use_cctld_negotiation = value

    def get_use_request_negotiation(self):
        return self.context.use_request_negotiation

    def set_use_request_negotiation(self, value):
        self.context.use_request_negotiation = value

    default_language = property(get_default_language,
                                set_default_language)

    use_combined_language_codes = property(get_use_combined_language_codes,
                                           set_use_combined_language_codes)

    available_languages = property(get_available_languages,
                                   set_available_languages)

    use_content_negotiation = property(get_use_content_negotiation,
                                       set_use_content_negotiation)
    use_path_negotiation = property(get_use_path_negotiation,
                                    set_use_path_negotiation)
    use_cookie_negotiation = property(get_use_cookie_negotiation,
                                      set_use_cookie_negotiation)
    authenticated_users_only = property(get_authenticated_users_only,
                                        set_authenticated_users_only)
    set_cookie_everywhere = property(get_set_cookie_everywhere,
                                     set_set_cookie_everywhere)
    use_subdomain_negotiation = property(get_use_subdomain_negotiation,
                                         set_use_subdomain_negotiation)
    use_cctld_negotiation = property(get_use_cctld_negotiation,
                                     set_use_cctld_negotiation)
    use_request_negotiation = property(get_use_request_negotiation,
                                       set_use_request_negotiation)


class LanguageControlPanel(ControlPanelForm):

    form_fields = FormFields(ILanguageSelectionSchema)
    form_fields['default_language'].custom_widget = LanguageDropdownChoiceWidget

    label = _(u"heading_language_settings", default="Language Settings")
    description = _(u"description_language_settings",
                    default="Settings related to interface languages and "
                            "content translations.")
    form_name = _(u"heading_language_settings", default="Language Settings")

