===========================
Terms & Conditions Scenario
===========================

Imports::

    >>> import datetime
    >>> from decimal import Decimal
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules, set_user
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company

Install terms_and_conditions::

    >>> config = activate_modules('terms_and_conditions')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Get the admin user::

    >>> User = Model.get('res.user')
    >>> admin_user, = User.find([('login', '=', 'admin')])

Reload the context::

    >>> config._context = User.get_preferences(True, config.context)

Create terms and conditions::

    >>> set_user(admin_user)
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
