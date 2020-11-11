# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Payment return supplier credit note',
    'summary': """
        This module allows to validate payments 
        of credit notes from suppliers.""",

    'author': 'Calyx Servicios S.A., Odoo Community Association (OCA)',
    'maintainers': ['miltonguzmanf@gmail.com'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    'category': 'Technical Settings',
    'version': '11.0.1.0.0',
    # see https://odoo-community.org/page/development-status
    'development_status': 'Production/Stable',

    'application': False,
    'installable': True,

    'depends': ['base_setup', 'product'],

    # 'data': [
    #     'security/ir.model.access.csv',
    #     'views/views.xml',
    #     'views/templates.xml',
    # ],
}
