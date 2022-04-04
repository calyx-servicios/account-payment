# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Account Payment Search by Amount',
    'summary': """
        search amount in account payment""",

    'author': 'Calyx Servicios S.A., Odoo Community Association (OCA)',
    'maintainers': ['<Github/Gitlab Username/s>'],

    'website': 'https://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Account',
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
    'depends': ['base', 'account_payment_group'],

    # always loaded
    'data': [
        'views/account_payment_group.xml',
    ],

    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
