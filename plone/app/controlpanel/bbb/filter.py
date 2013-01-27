from zope.component import adapts
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from zope.interface import implements
from Products.PortalTransforms.transforms.safe_html import VALID_TAGS
from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.interfaces import IFilterSchema
from Products.CMFPlone.interfaces import IPloneSiteRoot

XHTML_TAGS = set(
    'a abbr acronym address area b base bdo big blockquote body br '
    'button caption cite code col colgroup dd del div dfn dl dt em '
    'fieldset form h1 h2 h3 h4 h5 h6 head hr html i img input ins kbd '
    'label legend li link map meta noscript object ol optgroup option '
    'p param pre q samp script select small span strong style sub sup '
    'table tbody td textarea tfoot th thead title tr tt ul var'.split())


class FilterControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IFilterSchema)

    def __init__(self, context):
        super(FilterControlPanelAdapter, self).__init__(context)
        self.context = context
        self.transform = getattr(
            getToolByName(context, 'portal_transforms'), 'safe_html')
        self.kupu_tool = getToolByName(context, 'kupu_library_tool', None)

    def _settransform(self, **kwargs):
        # Cannot pass a dict to set transform parameters, it has
        # to be separate keys and values
        # Also the transform requires all dictionary values to be set
        # at the same time: other values may be present but are not
        # required.
        for k in ('valid_tags', 'nasty_tags'):
            if k not in kwargs:
                kwargs[k] = self.transform.get_parameter_value(k)

        for k in list(kwargs):
            if isinstance(kwargs[k], dict):
                v = kwargs[k]
                kwargs[k+'_key'] = v.keys()
                kwargs[k+'_value'] = [str(s) for s in v.values()]
                del kwargs[k]
        self.transform.set_parameters(**kwargs)
        self.transform._p_changed = True
        self.transform.reload()

    @apply
    def nasty_tags():
        def get(self):
            return sorted(self.transform.get_parameter_value('nasty_tags'))
        def set(self, value):
            value = dict.fromkeys(value, 1)
            valid = self.transform.get_parameter_value('valid_tags')
            for v in value:
                if v in valid:
                    del valid[v]
            self._settransform(nasty_tags=value, valid_tags=valid)
        return property(get, set)

    @apply
    def stripped_tags():
        def get(self):
            valid = set(self.transform.get_parameter_value('valid_tags'))
            stripped = XHTML_TAGS - valid
            return sorted(stripped)
        def set_(self, value):
            valid = dict(self.transform.get_parameter_value('valid_tags'))
            stripped = set(value)
            for v in XHTML_TAGS:
                if v in stripped:
                    if v in valid:
                        del valid[v]
                else:
                    valid[v] = VALID_TAGS.get(v, 1)

            # Nasty tags must never be valid
            for v in self.nasty_tags:
                if v in valid:
                    del valid[v]
            self._settransform(valid_tags=valid)
            # Set kupu attribute for backwards compatibility
            if self.kupu_tool is not None:
                self.kupu_tool.set_stripped_tags(value)

        return property(get, set_)

    @apply
    def custom_tags():
        def get(self):
            valid = set(self.transform.get_parameter_value('valid_tags'))
            custom = valid - XHTML_TAGS
            return sorted(custom)
        def set_(self, value):
            valid = dict(self.transform.get_parameter_value('valid_tags'))
            # Remove all non-standard tags
            for v in valid.keys():
                if v not in XHTML_TAGS:
                    del valid[v]
            # Now add in the custom tags
            for v in value:
                if v not in valid:
                    valid[v] = 1

            self._settransform(valid_tags=valid)

        return property(get, set_)


    @apply
    def style_whitelist():
        def get(self):
            return self.transform.get_parameter_value('style_whitelist')
        def set(self, value):
            self._settransform(style_whitelist = list(value))
            # Set kupu attribute for backwards compatibility
            if self.kupu_tool is not None:
                self.kupu_tool.style_whitelist = list(value)
        return property(get, set)

    @apply
    def class_blacklist():
        '''Ideally the form should allow setting a class whitelist,
        but that will have to be added later.'''
        def get(self):
            return self.transform.get_parameter_value('class_blacklist')
        def set(self, value):
            self._settransform(class_blacklist = list(value))
            # Set kupu attribute for backwards compatibility
            if self.kupu_tool is not None:
                self.kupu_tool.class_blacklist = list(value)
        return property(get, set)

    @apply
    def stripped_attributes():
        def get(self):
            return self.transform.get_parameter_value('stripped_attributes')
        def set(self, value):
            self._settransform(stripped_attributes = value)
            # Set kupu attribute for backwards compatibility
            if self.kupu_tool is not None:
                self.kupu_tool.set_stripped_attributes(value)
        return property(get, set)

    @apply
    def stripped_combinations():
        def get(self):
            stripped = []
            sc = self.transform.get_parameter_value('stripped_combinations')
            for k in sc.keys():
                stripped.append(TagAttrPair(k, sc[k]))
            return stripped
        def set(self, value):
            stripped = []
            strippeddict = {}
            for ta in value:
                strippeddict[ta.tags] = ta.attributes
                tags = ta.tags.replace(',', ' ').split()
                attributes = ta.attributes.replace(',', ' ').split()
                stripped.append((tags,attributes))

            self._settransform(stripped_combinations = strippeddict)
            # Set kupu attribute for backwards compatibility
            if self.kupu_tool is not None:
                self.kupu_tool.set_stripped_combinations(stripped)
        return property(get, set)