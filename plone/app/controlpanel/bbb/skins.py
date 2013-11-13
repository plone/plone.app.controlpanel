from zope.component import adapts
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.interfaces import ISkinsSchema


class SkinsControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ISkinsSchema)

    def __init__(self, context):
        super(SkinsControlPanelAdapter, self).__init__(context)
        self.context = getToolByName(context, 'portal_skins')
        self.jstool = getToolByName(context, 'portal_javascripts')
        self.csstool = getToolByName(context, 'portal_css')
        ptool = getToolByName(context, 'portal_properties')
        self.props = ptool.site_properties
        self.themeChanged = False

    def get_theme(self):
        return self.context.getDefaultSkin()

    def set_theme(self, value):
        self.themeChanged = True
        self.context.default_skin = value

    theme = property(get_theme, set_theme)

    def _update_jsreg_mark_special(self):
        self.jstool.getResource('mark_special_links.js').setEnabled(
            self.mark_special_links or self.ext_links_open_new_window
            )
        self.jstool.cookResources()

    def get_mark_special_links(self):
        msl = getattr(self.props, 'mark_special_links', False)
        if msl == 'true':
            return True
        return False

        # return self.jstool.getResource('mark_special_links.js').getEnabled()

    def set_mark_special_links(self, value):
        if value:
            mark_special_links='true'
        else:
            mark_special_links='false'
        if self.props.hasProperty('mark_special_links'):
            self.props.manage_changeProperties(mark_special_links=mark_special_links)
        else:
            self.props.manage_addProperty('mark_special_links', mark_special_links, 'string')
        self._update_jsreg_mark_special()

    mark_special_links = property(get_mark_special_links,
                                  set_mark_special_links)

    def get_ext_links_open_new_window(self):
        elonw = self.props.external_links_open_new_window
        if elonw == 'true':
            return True
        return False

    def set_ext_links_open_new_window(self, value):
        if value:
            self.props.manage_changeProperties(external_links_open_new_window='true')
        else:
            self.props.manage_changeProperties(external_links_open_new_window='false')
        self._update_jsreg_mark_special()

    ext_links_open_new_window = property(get_ext_links_open_new_window,
                                         set_ext_links_open_new_window)

    def get_icon_visibility(self):
        return self.props.icon_visibility

    def set_icon_visibility(self, value):
        self.props.manage_changeProperties(icon_visibility=value)

    icon_visibility = property(get_icon_visibility, set_icon_visibility)

    def get_use_popups(self):
        return self.jstool.getResource('popupforms.js').getEnabled()
        return self.csstool.getResource('++resource++plone.app.jquerytools.overlays.css').getEnabled()

    def set_use_popups(self, value):
        self.jstool.getResource('popupforms.js').setEnabled(value)
        self.jstool.cookResources()
        self.csstool.getResource('++resource++plone.app.jquerytools.overlays.css').setEnabled(value)
        self.csstool.cookResources()

    use_popups = property(get_use_popups, set_use_popups)
