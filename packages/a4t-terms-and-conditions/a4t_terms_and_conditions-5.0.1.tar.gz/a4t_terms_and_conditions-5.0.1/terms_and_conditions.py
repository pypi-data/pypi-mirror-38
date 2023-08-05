# -*- coding: utf-8 -*-
# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields, \
    sequence_ordered
from trytond.pool import Pool
from trytond.pyson import Eval, If
from trytond.transaction import Transaction

__all__ = ['TermsAndConditions', 'TermsAndConditionsLine',
           'TermsAndConditionsArticle']

LEVELS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ]

class TermsAndConditions(ModelSQL, ModelView):
    'Terms & Conditions'
    __name__ = 'terms_and_conditions'
    name = fields.Char('Name', select=True, required=True,
        help='The name of this T&C definition.')
    company = fields.Many2One('company.company', 'Company', required=True,
        select=True, domain=[
            ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', -1)),
            ],
        help=("Make the terms and conditions belong to the company."))
    lines = fields.One2Many('terms_and_conditions.line', 'tandc',
        'Lines of Terms & Conditions',)

    @staticmethod
    def default_company():
        return Transaction().context.get('company')


class TermsAndConditionsLine(sequence_ordered(), ModelSQL, ModelView):
    'Relation between Terms & Conditions definition and article'
    __name__ = 'terms_and_conditions.line'
    level = fields.Selection(LEVELS, 'Level', required=True,
        help = "Level in the hierarchy of articles. Essentially used to "
               "hierarchy articles when printing ('1' is the highest "
               "level, '6' is the lowest).")
    tandc = fields.Many2One('terms_and_conditions', 'Terms & Conditions',
        ondelete='CASCADE', select=True)
    article = fields.Many2One('terms_and_conditions.article', 'Article',
        ondelete='CASCADE', select=True, required=True,)

    @staticmethod
    def default_level():
        return '1'

    def get_rec_name(self, name):
        return self.article.name

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('article.name',) + tuple(clause[1:])]


class TermsAndConditionsArticle(ModelSQL, ModelView):
    'Articles of Terms & Conditions'
    __name__ = 'terms_and_conditions.article'
    name = fields.Char('Name', select=True, required=True, translate=True,
        help='The name of this article.')
    title = fields.Char('Title', select=True, required=True, translate=True,
        help='The title of this article.')
    content = fields.Text('Content', translate=True,
        help='Content of the article.')

    @fields.depends('name', 'title')
    def on_change_name(self):
        if not self.title:
            self.title = self.name
