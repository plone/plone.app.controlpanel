Introduction
============

This package provides various control panels for Plone and some
infrastrucuture to make it as easy as possible to create those with the help of z3c.form and plone.app.registry.

All control panel related settings are stored in plone.app.registry and
can be looked up like this:

  >>> site_settings = registry.forInterface(ISiteSchema)
  >>> site_settings.site_title
  u'Plone site'

If you want to change the settings, just change the attribute::

  >>> site_settings.site_title = 'My Plone site'


Site Control Panel
------------------

  >>> from plone.registry.interfaces import IRegistry
  >>> from zope.component import getUtility
  >>> from plone.app.controlpanel.interfaces import ISiteSchema
  >>> registry = getUtility(IRegistry)

  >>> site_settings = registry.forInterface(ISiteSchema)
  >>> site_settings.site_title = u'My Site'
  >>> site_settings.description_title = u'This is my site'
  >>> site_settings.exposeDCMetaTags = True
  >>> site_settings.enable_sitemap = True
  >>> site_settings.webstats_js = u'<script>a=1</script>'


Editing Control Panel
---------------------

    visible_ids
    default_editor
    ext_editor
    enable_link_integrity_checks
    lock_on_ttw_edit



