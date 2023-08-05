# -*- coding: utf-8 -*-
# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

__all__ = ['Configuration', 'ConfigurationSaleTermsAndConditions']


class Configuration(CompanyMultiValueMixin, metaclass=PoolMeta):
    __name__ = 'sale.configuration'
    sale_tandc = fields.MultiValue(fields.Many2One(
            'terms_and_conditions', "Terms & Conditions of sale",
            help="The default Terms & Conditions of new sale.",
            domain=[
                ('company', '=', Eval('context', {}).get('company', -1)),
                ],
            states={
                'invisible': ~Eval('context', {}).get('company'),
                }))


class ConfigurationSaleTermsAndConditions(ModelSQL, CompanyValueMixin):
    "Sale Configuration Sale Terms & Conditions"
    __name__ = 'sale.configuration.sale_tandc'
    sale_tandc = fields.Many2One(
        'terms_and_conditions', "Terms & Conditions",
        domain=[
            ('company', '=', Eval('company', -1)),
            ],
        depends=['company'])
