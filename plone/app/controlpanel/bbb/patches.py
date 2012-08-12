from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from Products.CMFPlone.PropertiesTool import SimpleItemWithProperties

from plone.app.controlpanel.interfaces import IEditingSchema
from plone.app.controlpanel.interfaces import IMailSchema
from plone.app.controlpanel.interfaces import INavigationSchema


def _setPropValue(self, id, value):
    super(SimpleItemWithProperties, self)._setPropValue(id, value)
    registry = queryUtility(IRegistry, context=self)
    if registry:
        if id in IEditingSchema.names():
            settings = registry.forInterface(IEditingSchema)
            setattr(settings, id, value)
        if id in IMailSchema.names():
            settings = registry.forInterface(IMailSchema)
            setattr(settings, id, value)
        if id in INavigationSchema.names():
            settings = registry.forInterface(INavigationSchema)
            setattr(settings, id, value)


def manage_makeChanges(
        self, title, smtp_host, smtp_port, smtp_uid='',
        smtp_pwd='', smtp_queue=False, smtp_queue_directory='/tmp',
        force_tls=False, REQUEST=None):
    #super(MailBase, self).manage_makeChanges(
    #    title,
    #    smtp_host,
    #    smtp_port,
    #    smtp_uid,
    #    smtp_pwd,
    #    smtp_queue,
    #    smtp_queue_directory,
    #    force_tls,
    #    REQUEST)
    registry = queryUtility(IRegistry, context=self)
    settings = registry.forInterface(IMailSchema)
    if registry:
        if smtp_host:
            setattr(settings, "smtp_host", smtp_host.decode("utf-8"))
        if smtp_port:
            setattr(settings, "smtp_port", smtp_port)
        if smtp_uid:
            setattr(settings, "smtp_userid", smtp_uid)
        if smtp_pwd:
            setattr(settings, "smtp_pass", smtp_pwd)
