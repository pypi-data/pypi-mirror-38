# -*- coding: utf-8 -*-
# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from trytond.pool import Pool
from .terms_and_conditions import *


def register():
    Pool.register(
        TermsAndConditions,
        TermsAndConditionsLine,
        TermsAndConditionsArticle,
        module='terms_and_conditions', type_='model')
