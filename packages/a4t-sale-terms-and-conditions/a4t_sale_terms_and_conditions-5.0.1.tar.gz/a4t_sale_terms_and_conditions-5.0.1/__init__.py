# -*- coding: utf-8 -*-
# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from trytond.pool import Pool
from .party import *
from .sale import *
from . import configuration


def register():
    Pool.register(
        Party,
        PartySaleTermsAndConditions,
        Sale,
        configuration.Configuration,
        configuration.ConfigurationSaleTermsAndConditions,
        module='sale_terms_and_conditions', type_='model')
