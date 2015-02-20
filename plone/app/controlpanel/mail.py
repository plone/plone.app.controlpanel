# Control panels for Plone 5 have been moved to CMFPlone. We keep those imports
# for backwards compatibility.
from Products.CMFPlone.interfaces import IMailSchema  # noqa
from Products.CMFPlone.controlpanel.mail import MailControlPanel  # noqa
from Products.CMFPlone.controlpanel.bbb.mail import MailControlPanelAdapter  # noqa
