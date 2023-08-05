# -*- coding: utf-8 -*-
# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
import logging
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.modules.company import CompanyReport

__all__ = ['Sale']
logger = logging.getLogger(__name__)


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    tandc = fields.Many2One('terms_and_conditions',
        'Terms & Conditions of Sale',
        states={
            'readonly': Eval('state') == 'cancel',
            },
        domain=[('company', '=', Eval('company'))],
        depends=['state', 'company'], select=True,
        help='Terms & Conditions associated to this sale.')

    def on_change_party(self):
        pool = Pool()
        Configuration = pool.get('sale.configuration')
        super(Sale, self).on_change_party()
        if self.party and self.party.sale_tandc:
            self.tandc = self.party.sale_tandc
        else:
            config = Configuration(1)
            self.tandc = config.sale_tandc
