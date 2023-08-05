# -*- coding: utf-8 -*-
# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from trytond import backend
from trytond.model import ModelSQL, fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta, Pool
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

__all__ = ['Party', 'PartySaleTermsAndConditions']


class Party(CompanyMultiValueMixin, metaclass=PoolMeta):
    __name__ = 'party.party'
    sale_tandc = fields.MultiValue(fields.Many2One(
            'terms_and_conditions', "Terms & Conditions of sale",
            help="The default Terms & Conditions of new sale.",
            domain=[
                ('company', '=', Eval('context', {}).get('company', -1)),
                ],
            states={
                'invisible': ~Eval('context', {}).get('company'),
                }))
    sale_tandcs = fields.One2Many(
        'party.party.sale_tandc', 'party', "Terms & Conditions of sale")

    @classmethod
    def default_sale_tandc(cls, **pattern):
        pool = Pool()
        Configuration = pool.get('sale.configuration')
        config = Configuration(1)
        tandc = config.get_multivalue('sale_tandc', **pattern)
        return tandc.id if tandc else None


class PartySaleTermsAndConditions(ModelSQL, CompanyValueMixin):
    "Party Sale Terms & Conditions"
    __name__ = 'party.party.sale_tandc'
    party = fields.Many2One(
        'party.party', "Party", ondelete='CASCADE', select=True)
    sale_tandc = fields.Many2One(
        'terms_and_conditions', "Terms & Conditions of sale",
        domain=[
            ('company', '=', Eval('company', -1)),
            ],
        depends=['company'])

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(PartySaleTermsAndConditions, cls).__register__(module_name)
