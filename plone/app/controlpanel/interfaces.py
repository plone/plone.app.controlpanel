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


class IMailSchema(Interface):
    """Combined schema for the adapter lookup.
    """

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
