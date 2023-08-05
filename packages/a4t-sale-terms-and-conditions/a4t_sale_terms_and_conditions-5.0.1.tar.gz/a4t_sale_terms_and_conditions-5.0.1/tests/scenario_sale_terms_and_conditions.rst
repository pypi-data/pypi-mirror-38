================================
Sale Terms & Conditions Scenario
================================

Imports::

    >>> import datetime
    >>> from decimal import Decimal
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules, set_user
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term

Install sale_terms_and_conditions::

    >>> config = activate_modules('sale_terms_and_conditions')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create sale user::

    >>> User = Model.get('res.user')
    >>> Group = Model.get('res.group')
    >>> sale_user = User()
    >>> sale_user.name = 'Sale'
    >>> sale_user.login = 'sale'
    >>> sale_user.main_company = company
    >>> sale_group, = Group.find([('name', '=', 'Sales')])
    >>> sale_user.groups.append(sale_group)
    >>> sale_user.save()

    >>> sale_admin = User()
    >>> sale_admin.name = 'Sale Admin'
    >>> sale_admin.login = 'sale_admin'
    >>> sale_admin.main_company = company
    >>> sale_admin_group, = Group.find([('name', '=', 'Sales Administrator')])
    >>> sale_admin.groups.append(sale_admin_group)
    >>> sale_admin.save()

Reload the context::

    >>> config._context = User.get_preferences(True, config.context)

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.save()
    >>> customer_without_terms_and_conditions = Party(
    ...     name='Customer without terms and conditions')
    >>> customer_without_terms_and_conditions.save()

Create account category::

    >>> ProductCategory = Model.get('product.category')
    >>> account_category = ProductCategory(name="Account Category")
    >>> account_category.accounting = True
    >>> account_category.account_expense = expense
    >>> account_category.account_revenue = revenue
    >>> account_category.save()

Create product::

    >>> ProductUom = Model.get('product.uom')
    >>> unit, = ProductUom.find([('name', '=', 'Unit')])
    >>> ProductTemplate = Model.get('product.template')

    >>> template = ProductTemplate()
    >>> template.name = 'product'
    >>> template.default_uom = unit
    >>> template.type = 'goods'
    >>> template.purchasable = True
    >>> template.salable = True
    >>> template.list_price = Decimal('10')
    >>> template.account_category = account_category
    >>> template.save()
    >>> product, = template.products

    >>> template = ProductTemplate()
    >>> template.name = 'service'
    >>> template.default_uom = unit
    >>> template.type = 'service'
    >>> template.salable = True
    >>> template.list_price = Decimal('30')
    >>> template.account_category = account_category
    >>> template.save()
    >>> service, = template.products

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create terms and conditions and assign it to customer

    >>> Article = Model.get('terms_and_conditions.article')
    >>> article1 = Article(name='Article 1', title='Article 1',
    ...     content='Content 1')
    >>> article1.save()
    >>> article2 = Article(name='Article 2', title='Article 2',
    ...     content='Content 2')
    >>> article2.save()
    >>> article3 = Article(name='Article 3', title='Article 3',
    ...     content='Content 3')
    >>> article2.save()
    >>> TandC = Model.get('terms_and_conditions')
    >>> tandc = TandC(name='Terms & Conditions')
    >>> tandc.company = company
    >>> tandc_line = tandc.lines.new(article=article1)
    >>> tandc_line.level = '1'
    >>> tandc_line = tandc.lines.new(article=article2)
    >>> tandc_line.level = '1'
    >>> tandc_line = tandc.lines.new(article=article3)
    >>> tandc_line.level = '1'
    >>> tandc_line.article = article3
    >>> tandc.save()
    >>> customer.sale_tandc = tandc
    >>> customer.save()

Use the terms and conditions on sale::

    >>> set_user(sale_user)
    >>> Sale = Model.get('sale.sale')
    >>> sale = Sale()
    >>> sale.party = customer
    >>> sale.tandc == tandc
    True

Create a sale terms and conditions and assign to configuration::

    >>> set_user(sale_admin)
    >>> sale_tandc = TandC(name='Terms & Conditions 2')
    >>> sale_tandc.company = company
    >>> sale_tandc_line = sale_tandc.lines.new()
    >>> sale_tandc_line.level = '1'
    >>> sale_tandc_line.article = article1
    >>> sale_tandc.save()
    >>> Configuration = Model.get('sale.configuration')
    >>> config = Configuration()
    >>> config.sale_tandc = sale_tandc
    >>> config.save()

Use the sale terms ans conditions on sale::

    >>> set_user(sale_user)
    >>> sale.party = customer_without_terms_and_conditions
    >>> sale.tandc == sale_tandc
    True
