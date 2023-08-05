# This file is part of Adiczion's Tryton Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.

try:
    from trytond.modules.sale_terms_and_conditions.tests.test_sale_terms_and_conditions import suite
except ImportError:
    from .test_sale_terms_and_conditions import suite

__all__ = ['suite']
