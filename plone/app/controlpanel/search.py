from plone.fieldsets.fieldsets import FormFieldsets
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import Tuple
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFPlone import PloneMessageFactory as _

from form import ControlPanelForm
from widgets import MultiCheckBoxThreeColumnWidget as MCBThreeColumnWidget


anon_auth_items = (('anon', _(u'anonymous users')),
                   ('auth', _(u'logged in users'),))

anon_auth_terms = [SimpleTerm(item[0], title=item[1]) for item in
                   anon_auth_items]

AnonAuthVocabulary = SimpleVocabulary(anon_auth_terms)

class IBaseSearchSchema(Interface):

    enable_livesearch = Bool(
        title=_(u'Enable LiveSearch'),
        description=_(u"Enables the LiveSearch feature, which shows live "
                       "results if the browser supports JavaScript."),
        default=False,
        required=True
        )

    types_not_searched = Tuple(
        title=_(u"Define the types to be shown in the site and searched"),
        description=_(u"Define the types that should be searched and be "
                       "available in the user facing part of the site. "
                       "Note that if new content types are installed, they "
                       "will be enabled by default unless explicitly turned "
                       "off here or by the relevant installer."),
        required=True,
        missing_value=tuple(),
        value_type=Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")
        )


class ISearchSchema(IBaseSearchSchema):
    ''' Base search form options '''


searchset = FormFieldsets(IBaseSearchSchema)
searchset.id = 'search'
searchset.label = _("Search settings")

class SearchControlPanel(ControlPanelForm):

    form_fields = FormFieldsets(searchset)
    form_fields['types_not_searched'].custom_widget = MCBThreeColumnWidget
    form_fields['types_not_searched'].custom_widget.cssClass='label'

    label = _("Search settings")
    description = _("Search settings for this site.")
    form_name = _("Search settings")
