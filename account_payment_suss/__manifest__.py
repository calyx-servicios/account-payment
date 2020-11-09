# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Account Payment SUSS',
    'summary': """
        Automatization of Regime 2682 in Payments""",

    'author': 'Calyx Servicios S.A., Odoo Community Association (OCA)',
    'maintainers': ['FedericoGregori'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '11.0.1.0.0',
    # see https://odoo-community.org/page/development-status
    'development_status': 'Production/Stable',

    'application': False,
    'installable': True,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'account',
        'account_payment_group',
        'account_withholding',
        'account_withholding_automatic',
        'l10n_ar_account_withholding'
    ],

    # always loaded
    'data': [
        'data/account_account_tag.xml',
        'data/account_tax_group.xml',
        'data/account_tax.xml',
        'views/account_payment_group_view.xml',
        'views/product_template_view.xml',
        'views/account_tax_view.xml',
    ],

    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
