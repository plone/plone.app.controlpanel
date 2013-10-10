# -*- coding: utf-8 -*-
from plone.app.controlpanel.widgets import ReverseCheckBoxWidget
from z3c.form.testing import TestRequest
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import unittest2 as unittest


class ReverseCheckboxWidgetTest(unittest.TestCase):

    def setUp(self):
        self.request = TestRequest()
        self.widget = ReverseCheckBoxWidget(self.request)
        self.widget.name = 'from.widget.reversecheckbox'
        self.widget.terms = SimpleVocabulary.fromValues(
            ['spam', 'and', 'eggs'])

    def test_is_checked_with_term_in_value(self):
        term = SimpleTerm('spam', 'spam', 'spam')
        self.widget.value = ('spam', 'eggs')
        self.assertFalse(self.widget.isChecked(term))

    def test_is_checked_with_term_not_in_value(self):
        term = SimpleTerm('eggs', 'eggs', 'eggs')
        self.widget.value = ('spam', 'and')
        self.assertTrue(self.widget.isChecked(term))

    def test_extract_empty_marker_gives_all_terms(self):
        self.request.form.update(
            {'from.widget.reversecheckbox-empty-marker': '1'})
        self.assertEquals(['spam', 'and', 'eggs'], self.widget.extract())

    def test_extract_default_value(self):
        self.request.form.update({'from.widget.reversecheckbox': ['DEFAULT']})
        self.assertEquals(['DEFAULT'],
                          self.widget.extract(default=['DEFAULT']))

    def test_extract_gives_reverse_terms(self):
        self.request.form.update({'from.widget.reversecheckbox': ['spam']})
        self.assertEquals(['and', 'eggs'], self.widget.extract())
