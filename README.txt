Introduction
============

This package provides various control panels for Plone and some
infrastrucuture to make it as easy as possible to create those with the help of z3c.form and plone.app.registry.

All control panel related settings are stored in plone.app.registry and
can be looked up like this::

  >>> from zope.component import getUtility
  >>> from plone.registry.interfaces import IRegistry
  >>> registry = getUtility(IRegistry)

  >>> from plone.app.controlpanel.interfaces import ISiteSchema
  >>> site_settings = registry.forInterface(ISiteSchema)
  >>> site_settings.site_title
  u'Plone site'

If you want to change the settings, just change the attribute::

  >>> site_settings.site_title = u'My Plone site'

  >>> site_settings.site_title
  u'My Plone site'


Editing Control Panel
---------------------

  >>> from plone.app.controlpanel.interfaces import IEditingSchema
  >>> editing_settings = registry.forInterface(IEditingSchema)

  >>> editing_settings.visible_ids = True
  >>> editing_settings.default_editor = 'TinyMCE'
  >>> editing_settings.ext_editor = True
  >>> editing_settings.enable_link_integrity_checks = True
  >>> editing_settings.lock_on_ttw_edit = True


Search Control Panel
--------------------

  >>> from plone.app.controlpanel.interfaces import ISearchSchema
  >>> site_settings = registry.forInterface(ISearchSchema)

  >>> site_settings.enable_livesearch = True
  >>> site_settings.types_not_searched = ('Discussion Item', 'Folder')


Site Control Panel
------------------

  >>> from plone.app.controlpanel.interfaces import ISiteSchema
  >>> site_settings = registry.forInterface(ISiteSchema)

  >>> site_settings.site_title = u'My Site'
  >>> site_settings.description_title = u'This is my site'
  >>> site_settings.exposeDCMetaTags = True
  >>> site_settings.enable_sitemap = True
  >>> site_settings.webstats_js = u'<script>a=1</script>'
