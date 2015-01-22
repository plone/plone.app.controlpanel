from plone.fieldsets.fieldsets import FormFieldsets

from zope.interface import Interface
from zope.interface import implements
from zope.schema import Choice
from zope.schema import Tuple

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import AllowedTypesWidget
from plone.app.controlpanel.widgets import MultiCheckBoxVocabularyWidget

from persistent import Persistent

try:
    from wicked.plone.registration import basic_type_regs as wicked_basic_type_regs
except ImportError:
    HAS_WICKED = False
else:
    HAS_WICKED = True

WICKED_SETTING_KEY="plone.app.controlpanel.wicked"

class WickedSettings(Persistent):
    """Settings for Wicked markup
    """
    types_enabled = []
    enable_mediawiki = False

if HAS_WICKED:
    wicked_type_regs = dict((factory.type, factory) for factory in \
                            wicked_basic_type_regs)

class WickedTypesVocabulary(object):
    """Vocabulary factory for wickedized portal types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ttool = getToolByName(context, 'portal_types')
        items = []
        # Pretty insane code, but wicked uses different internal names for
        # the types :(
        for t in ttool.listContentTypes():
            for reg in wicked_basic_type_regs:
                if reg.type_id == t:
                    items.append(SimpleTerm(reg.type, reg.type, ttool[t].Title()))
        return SimpleVocabulary(items)

WickedTypesVocabularyFactory = WickedTypesVocabulary()

#
# Markup types
#

class ITextMarkupSchema(Interface):

    default_type = Choice(title=_(u'Default format'),
        description=_(u"Select the default format of textfields for newly "
                       "created content objects."),
        default=u'text/html',
        missing_value=set(),
        vocabulary="plone.app.vocabularies.AllowableContentTypes",
        required=True)

    allowed_types = Tuple(title=_(u'Alternative formats'),
        description=_(u"Select which formats are available for users as "
                       "alternative to the default format. Note that if new "
                       "formats are installed, they will be enabled for text "
                       "fields by default unless explicitly turned off here "
                       "or by the relevant installer."),
        required=True,
        missing_value=set(),
        value_type=Choice(
            vocabulary="plone.app.vocabularies.AllowableContentTypes"))

#
# Wicked behaviour
#

class IWikiMarkupSchema(Interface):

    wiki_enabled_types = Tuple(title=_(u"Choose which types will have wiki "
                                        "behavior."),
                               description=_(u"Each type chosen will have a "
                                             "wiki enabled primary text area. "
                                             "At least one type must be chosen "
                                             "to turn wiki behavior on."),
                               required=False,
                               missing_value=tuple(),
                               value_type=Choice(vocabulary="plone.app.\
controlpanel.WickedPortalTypes"))

#
# Combined schemata and fieldsets
#

if HAS_WICKED:
    class IMarkupSchema(ITextMarkupSchema, IWikiMarkupSchema):
        """Combined schema for the adapter lookup.
        """
else:
    IMarkupSchema = ITextMarkupSchema


textset = FormFieldsets(ITextMarkupSchema)
textset.id = 'textmarkup'
textset.label = _(u'Text markup')

if HAS_WICKED:
    wikiset = FormFieldsets(IWikiMarkupSchema)
    wikiset.id = 'wiki'
    wikiset.label = _(u'Wiki behavior')

class MarkupControlPanel(ControlPanelForm):

    if HAS_WICKED:
        form_fields = FormFieldsets(textset, wikiset)
        form_fields['wiki_enabled_types'].custom_widget = MultiCheckBoxVocabularyWidget
    else:
        form_fields = FormFieldsets(textset)
    form_fields['allowed_types'].custom_widget = AllowedTypesWidget

    label = _("Markup settings")
    description = _("Lets you control what markup is available when editing "
                    "content.")
    form_name = _("Markup settings")
