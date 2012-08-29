from z3c.form import interfaces

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

    calendar_states = schema.List(
      title=_(u'Workflow states to show in the calendar'),
      required=True,
      default=['published'],
      value_type=schema.Choice(
          source="plone.app.vocabularies.WorkflowStates"))


class IEditingSchema(Interface):

    visible_ids = schema.Bool(
        title=_(u"Show 'Short Name' on content?"),
        description=_(u"Display and allow users to edit the "
             "'Short name' content identifiers, which form the "
             "URL part of a content item's address. Once "
             "enabled, users will then be able to enable this "
             "option in their preferences."),
        default=False,
        required=False)

    default_editor = schema.Choice(
        title=_(u'Default editor'),
        description=_(u"Select the default wysiwyg "
            "editor. Users will be able to choose their "
            "own or select to use the site default."),
        default=u'TinyMCE',
        missing_value=set(),
        vocabulary="plone.app.vocabularies.AvailableEditors",
        required=True)

    ext_editor = schema.Bool(
        title=_(u'Enable External Editor feature'),
        description=_(u"Determines if the external editor "
            "feature is enabled. This feature requires a "
            "special client-side application installed. The "
            "users also have to enable this in their "
            "preferences."),
        default=False,
        required=False)

    enable_inline_editing = schema.Bool(
        title=_(u"Enable inline editing"),
        description=_(u"Check this to enable "
                      "inline editing on the site."),
        default=False,
        required=False)

    enable_link_integrity_checks = schema.Bool(
        title=_(u"Enable link integrity checks"),
        description=_(u"Determines if the users should get "
            "warnings when they delete or move content that "
            "is linked from inside the site."),
        default=True,
        required=False)

    lock_on_ttw_edit = schema.Bool(
        title=_(u"Enable locking for through-the-web edits"),
        description=_(u"Disabling locking here will only "
              "affect users editing content through the "
              "Plone web UI.  Content edited via WebDAV "
              "clients will still be subject to locking."),
        default=True,
        required=False)


class IMailSchema(Interface):

    smtp_host = schema.TextLine(
        title=_(u'label_smtp_server',
                default=u'SMTP server'),
        description=_(u"help_smtp_server",
                     default=u"The address of your local "
                     "SMTP (outgoing e-mail) server. Usually "
                     "'localhost', unless you use an "
                     "external server to send e-mail."),
        default=u'localhost',
        required=True)

    smtp_port = schema.Int(
        title=_(u'label_smtp_port',
                default=u'SMTP port'),
        description=_(u"help_smtp_port",
                      default=u"The port of your local SMTP "
                      "(outgoing e-mail) server. Usually '25'."),
        default=25,
        required=True)

    smtp_userid = schema.TextLine(
        title=_(u'label_smtp_userid',
               default=u'ESMTP username'),
        description=_(u"help_smtp_userid",
                     default=u"Username for authentication "
                     "to your e-mail server. Not required "
                     "unless you are using ESMTP."),
        default=None,
        required=False)

    smtp_pass = schema.Password(
        title=_(u'label_smtp_pass',
               default=u'ESMTP password'),
        description=_(u"help_smtp_pass",
                     default=u"The password for the ESMTP "
                     "user account."),
        default=None,
        required=False)

    email_from_name = schema.TextLine(
        title=_(u"Site 'From' name"),
        description=_(u"Plone generates e-mail using "
                      "this name as the e-mail "
                      "sender."),
        default=None,
        required=True)

    email_from_address = schema.ASCII(
        title=_(u"Site 'From' address"),
        description=_(u"Plone generates e-mail using "
                      "this address as the e-mail "
                      "return address. It is also "
                      "used as the destination "
                      "address for the site-wide "
                      "contact form and the 'Send test "
                      "e-mail' feature."),
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
          u"By default, any content item in the root of the portal will be " +
          u"shown as a global section. If you turn this option off, only " +
          u"folders will be shown. This only has an effect if " +
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
            source="plone.app.vocabularies.ReallyUserFriendlyTypes")
        )

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
            source="plone.app.vocabularies.WorkflowStates")
        )

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


class ISecuritySchema(Interface):

    enable_self_reg = schema.Bool(
        title=_(u'Enable self-registration'),
        description=_(u"Allows users to register themselves on the site. If "
                      "not selected, only site managers can add new users."),
        default=False,
        required=False)

    enable_user_pwd_choice = schema.Bool(
        title=_(u'Let users select their own passwords'),
        description=_(u"If not selected, a URL will be generated and "
                      "e-mailed. Users are instructed to follow the link to "
                      "reach a page where they can change their password and "
                      "complete the registration process; this also verifies "
                      "that they have entered a valid email address."),
        default=False,
        required=False)

    enable_user_folders = schema.Bool(
        title=_(u'Enable User Folders'),
        description=_(u"If selected, home folders where users can create "
                      "content will be created when they log in."),
        default=False,
        required=False)

    allow_anon_views_about = schema.Bool(
        title=_(u"Allow anyone to view 'about' information"),
        description=_(u"If not selected only logged-in users will be able to "
                      "view information about who created an item and when it "
                      "was modified."),
        default=False,
        required=False)

    use_email_as_login = schema.Bool(
        title=_(u'Use email address as login name'),
        description=_(u"Allows new  users to login with their email address "
                      "instead of specifying a separate login name. (Existing "
                      "users must go to the @@personal-information page once "
                      "and save it before this setting has effect for them. "
                      "Or use the @@migrate-to-emaillogin page as a site "
                      "admin)"),
        default=False,
        required=False)
