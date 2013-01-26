
from zope import schema

from zope.interface import Attribute
from zope.interface import Interface

from plone.app.controlpanel import _


class IPloneControlPanelView(Interface):
    """A marker interface for views showing a controlpanel.
    """


class IPloneControlPanelForm(IPloneControlPanelView):
    """Forms using plone.app.controlpanel
    """

    def _on_save():
        """Callback mehod which can be implemented by control panels to
        react when the form is successfully saved. This avoids the need
        to re-define actions only to do some additional notification or
        configuration which cannot be handled by the normal schema adapter.

        By default, does nothing.
        """


class IConfigurationChangedEvent(Interface):
    """An event which is fired after a configuration setting has been changed.
    """

    context = Attribute("The configuration context which was changed.")

    data = Attribute("The configuration data which was changed.")


from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

weekdays = SimpleVocabulary([
    SimpleTerm(value=0, title=_(u'Monday')),
    SimpleTerm(value=1, title=_(u'Tuesday')),
    SimpleTerm(value=2, title=_(u'Wednesday')),
    SimpleTerm(value=3, title=_(u'Thursday')),
    SimpleTerm(value=4, title=_(u'Friday')),
    SimpleTerm(value=5, title=_(u'Saturday')),
    SimpleTerm(value=6, title=_(u'Sunday')),
])


class ICalendarSchema(Interface):

    firstweekday = schema.Choice(
        title=_(u'First day of week in the calendar'),
        default=0,
        vocabulary=weekdays,
        required=True)

    calendar_states = schema.Tuple(
        title=_(u'Workflow states to show in the calendar'),
        required=True,
        default=('published',),
        value_type=schema.Choice(
            source="plone.app.vocabularies.WorkflowStates"))


class IEditingSchema(Interface):

    visible_ids = schema.Bool(
        title=_(u"Show 'Short Name' on content?"),
        description=_(
            u"Display and allow users to edit the "
            u"'Short name' content identifiers, which form the "
            u"URL part of a content item's address. Once "
            u"enabled, users will then be able to enable this "
            u"option in their preferences."),
        default=False,
        required=False)

    default_editor = schema.Choice(
        title=_(u'Default editor'),
        description=_(
            u"Select the default wysiwyg "
            u"editor. Users will be able to choose their "
            u"own or select to use the site default."),
        default=u'TinyMCE',
        missing_value=set(),
        vocabulary="plone.app.vocabularies.AvailableEditors",
        required=True)

    ext_editor = schema.Bool(
        title=_(u'Enable External Editor feature'),
        description=_(
            u"Determines if the external editor "
            u"feature is enabled. This feature requires a "
            u"special client-side application installed. The "
            u"users also have to enable this in their "
            u"preferences."),
        default=False,
        required=False)

    enable_inline_editing = schema.Bool(
        title=_(u"Enable inline editing"),
        description=_(
            u"Check this to enable "
            u"inline editing on the site."),
        default=False,
        required=False)

    enable_link_integrity_checks = schema.Bool(
        title=_(u"Enable link integrity checks"),
        description=_(
            u"Determines if the users should get "
            u"warnings when they delete or move content that "
            u"is linked from inside the site."),
        default=True,
        required=False)

    lock_on_ttw_edit = schema.Bool(
        title=_(u"Enable locking for through-the-web edits"),
        description=_(
            u"Disabling locking here will only "
            u"affect users editing content through the "
            u"Plone web UI.  Content edited via WebDAV "
            u"clients will still be subject to locking."),
        default=True,
        required=False)


class ILanguageSchema(Interface):

    use_combined_language_codes = schema.Bool(
        title=_(
            u'label_allow_combined_language_codes',
            default=u"Show country-specific language variants"
        ),
        description=_(
            u"help_allow_combined_language_codes",
            default=u"Examples: pt-br (Brazilian Portuguese), "
                    u"en-us (American English) etc."
        ),
        default=False,
        required=False
    )

    default_language = schema.Choice(
        title=_(u"heading_site_language",
                default=u"Site language"),
        description=_(
            u"description_site_language",
            default=u"The language used for the content and the UI "
                    u"of this site."),
        default='en',
        required=True,
        vocabulary="plone.app.vocabularies.AvailableContentLanguages"
    )


class IMailSchema(Interface):

    smtp_host = schema.TextLine(
        title=_(
            u'label_smtp_server',
            default=u'SMTP server'),
        description=_(
            u"help_smtp_server",
            default=u"The address of your local "
                    u"SMTP (outgoing e-mail) server. Usually "
                    u"'localhost', unless you use an "
                    u"external server to send e-mail."),
        default=u'localhost',
        required=True)

    smtp_port = schema.Int(
        title=_(u'label_smtp_port',
                default=u'SMTP port'),
        description=_(u"help_smtp_port",
                      default=u"The port of your local SMTP "
                              u"(outgoing e-mail) server. Usually '25'."),
        default=25,
        required=True)

    smtp_userid = schema.TextLine(
        title=_(
            u'label_smtp_userid',
            default=u'ESMTP username'),
        description=_(
            u"help_smtp_userid",
            default=u"Username for authentication "
                    u"to your e-mail server. Not required "
                    u"unless you are using ESMTP."),
        default=None,
        required=False)

    smtp_pass = schema.Password(
        title=_(
            u'label_smtp_pass',
            default=u'ESMTP password'),
        description=_(
            u"help_smtp_pass",
            default=u"The password for the ESMTP "
                    u"user account."),
        default=None,
        required=False)

    email_from_name = schema.TextLine(
        title=_(u"Site 'From' name"),
        description=_(
            u"Plone generates e-mail using "
            u"this name as the e-mail "
            u"sender."),
        default=None,
        required=True)

    email_from_address = schema.ASCII(
        title=_(u"Site 'From' address"),
        description=_(
            u"Plone generates e-mail using "
            u"this address as the e-mail "
            u"return address. It is also "
            u"used as the destination "
            u"address for the site-wide "
            u"contact form and the 'Send test "
            u"e-mail' feature."),
        default=None,
        required=True)


class INavigationSchema(Interface):

    generate_tabs = schema.Bool(
        title=_(u"Automatically generate tabs"),
        description=_(
            u"By default, all items created at the root level will " +
            u"add to the global section navigation. You can turn this off " +
            u"if you prefer manually constructing this part of the " +
            u"navigation."),
        default=True,
        required=False)

    nonfolderish_tabs = schema.Bool(
        title=_(u"Generate tabs for items other than folders."),
        description=_(
            u"By default, any content item in the root of the portal will" +
            u"be shown as a global section. If you turn this option off, " +
            u"only folders will be shown. This only has an effect if " +
            u"'Automatically generate tabs' is enabled."),
        default=True,
        required=False)

    displayed_types = schema.Tuple(
        title=_(u"Displayed content types"),
        description=_(
            u"The content types that should be shown in the navigation and " +
            u"site map."),
        required=False,
        default=(),
        value_type=schema.Choice(
            source="plone.app.vocabularies.ReallyUserFriendlyTypes"
        ))

    filter_on_workflow = schema.Bool(
        title=_(u"Filter on workflow state"),
        description=_(
            u"The workflow states that should be shown in the navigation " +
            u"tree and the site map."),
        default=False,
        required=False)

    workflow_states_to_show = schema.Tuple(
        required=False,
        default=(),
        value_type=schema.Choice(
            source="plone.app.vocabularies.WorkflowStates"))

    show_excluded_items = schema.Bool(
        title=_(
            u"Show items normally excluded from navigation if viewing their " +
            u"children."),
        description=_(
            u"If an item has been excluded from navigation should it be " +
            u"shown in navigation when viewing content contained within it " +
            u"or within a subfolder."),
        default=True,
        required=False)


class ISearchSchema(Interface):

    enable_livesearch = schema.Bool(
        title=_(u'Enable LiveSearch'),
        description=_(
            u"Enables the LiveSearch feature, which shows live "
            u"results if the browser supports JavaScript."),
        default=True,
        required=True
    )

    types_not_searched = schema.Tuple(
        title=_(u"Define the types to be shown in the site and searched"),
        description=_(
            u"Define the types that should be searched and be "
            u"available in the user facing part of the site. "
            u"Note that if new content types are installed, they "
            u"will be enabled by default unless explicitly turned "
            u"off here or by the relevant installer."
        ),
        required=True,
        default=('ATBooleanCriterion', 'ATDateCriteria', 'ATDateRangeCriterion', 'ATListCriterion', 'ATPortalTypeCriterion', 'ATReferenceCriterion', 'ATSelectionCriterion', 'ATSimpleIntCriterion', 'ATSimpleStringCriterion', 'ATSortCriterion', 'ChangeSet', 'Discussion Item', 'Plone Site', 'TempFolder', 'ATCurrentAuthorCriterion', 'ATPathCriterion', 'ATRelativePathCriterion'),
        value_type=schema.Choice(
            source="plone.app.vocabularies.ReallyUserFriendlyTypes")
    )


class ISecuritySchema(Interface):

    enable_self_reg = schema.Bool(
        title=_(u'Enable self-registration'),
        description=_(
            u"Allows users to register themselves on the site. If "
            u"not selected, only site managers can add new users."),
        default=False,
        required=False)

    enable_user_pwd_choice = schema.Bool(
        title=_(u'Let users select their own passwords'),
        description=_(
            u"If not selected, a URL will be generated and "
            u"e-mailed. Users are instructed to follow the link to "
            u"reach a page where they can change their password and "
            u"complete the registration process; this also verifies "
            u"that they have entered a valid email address."),
        default=False,
        required=False)

    enable_user_folders = schema.Bool(
        title=_(u'Enable User Folders'),
        description=_(
            u"If selected, home folders where users can create "
            u"content will be created when they log in."),
        default=False,
        required=False)

    allow_anon_views_about = schema.Bool(
        title=_(u"Allow anyone to view 'about' information"),
        description=_(
            u"If not selected only logged-in users will be able to "
            u"view information about who created an item and when it "
            u"was modified."),
        default=False,
        required=False)

    use_email_as_login = schema.Bool(
        title=_(u'Use email address as login name'),
        description=_(
            u"Allows new  users to login with their email address "
            u"instead of specifying a separate login name. (Existing "
            u"users must go to the @@personal-information page once "
            u"and save it before this setting has effect for them. "
            u"Or use the @@migrate-to-emaillogin page as a site "
            u"admin)"),
        default=False,
        required=False)


from plone.locking.interfaces import ILockSettings


# XXX: Why does ISiteSchema inherit from ILockSettings here ???
class ISiteSchema(ILockSettings):

    site_title = schema.TextLine(
        title=_(u'Site title'),
        description=_(
            u"This shows up in the title bar of "
            u"browsers and in syndication feeds."),
        default=u'')

    site_description = schema.Text(
        title=_(u'Site description'),
        description=_(
            u"The site description is available "
            u"in syndicated content and in search engines. "
            u"Keep it brief."),
        default=u'',
        required=False)

    exposeDCMetaTags = schema.Bool(
        title=_(u"Expose Dublin Core metadata"),
        description=_(u"Exposes the Dublin Core properties as metatags."),
        default=False,
        required=False)

    enable_sitemap = schema.Bool(
        title=_(u"Expose sitemap.xml.gz"),
        description=_(
            u"Exposes your content as a file "
            u"according to the sitemaps.org standard. You "
            u"can submit this to compliant search engines "
            u"like Google, Yahoo and Microsoft. It allows "
            u"these search engines to more intelligently "
            u"crawl your site."),
        default=False,
        required=False)

    webstats_js = schema.SourceText(
        title=_(u'JavaScript for web statistics support'),
        description=_(
            u"For enabling web statistics support "
            u"from external providers (for e.g. Google "
            u"Analytics). Paste the code snippets provided. "
            u"It will be included in the rendered HTML as "
            u"entered near the end of the page."),
        default=u'',
        required=False)


ICON_VISIBILITY_CHOICES = {
    _(u"Only for users who are logged in"): 'authenticated',
    _(u"Never show icons"): 'disabled',
    _(u"Always show icons"): 'enabled',
}

ICON_VISIBILITY_VOCABULARY = SimpleVocabulary(
    [SimpleTerm(v, v, k) for k, v in ICON_VISIBILITY_CHOICES.items()])


class ISkinsSchema(Interface):

    theme = schema.Choice(
        title=_(u'Default theme'),
        description=_(u'Select the default theme for the site.'),
        required=True,
        missing_value=tuple(),
        default="Sunburst Theme",
        vocabulary="plone.app.vocabularies.Skins")

    mark_special_links = schema.Bool(
        title=_(u'Mark external links'),
        description=_(
            u"If enabled all external links "
            u"will be marked with link type "
            u"specific icons."),
        default=True)

    ext_links_open_new_window = schema.Bool(
        title=_(u"External links open in new window"),
        description=_(
            u"If enabled all external links in the content region open in a "
            u"new window."),
        default=False)

    icon_visibility = schema.Choice(
        title=_(u'Show content type icons'),
        description=_(
            u"If disabled the content icons in folder listings and portlets "
            u"won't be visible."),
        default='enabled',
        vocabulary=ICON_VISIBILITY_VOCABULARY)

    use_popups = schema.Bool(
        title=_(u'Use popup overlays for simple forms'),
        description=_(
            u"If enabled popup overlays will be used for simple forms like "
            u"login, contact and delete confirmation."),
        default=True)


class IUserGroupsSettingsSchema(Interface):

    many_groups = schema.Bool(title=_(u'Many groups?'),
                       description=_(u"Determines if your Plone is optimized "
                           "for small or large sites. In environments with a "
                           "lot of groups it can be very slow or impossible "
                           "to build a list all groups. This option tunes the "
                           "user interface and behaviour of Plone for this "
                           "case by allowing you to search for groups instead "
                           "of listing all of them."),
                       default=False)

    many_users = schema.Bool(title=_(u'Many users?'),
                      description=_(u"Determines if your Plone is optimized "
                          "for small or large sites. In environments with a "
                          "lot of users it can be very slow or impossible to "
                          "build a list all users. This option tunes the user "
                          "interface and behaviour of Plone for this case by "
                          "allowing you to search for users instead of "
                          "listing all of them."),
                      default=False)
