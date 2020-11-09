# -*- coding: utf-8 -*-
{
    'name': "Account Payment Group Report Extend",

    'summary': """
        Extiende el reporte de pagos para agregar detalles """,

    'description': """
        
    """,

    'author': "Calyx",
    'website': "http://www.calyxservicios.com.ar",

    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
                'base',
                'account_payment_group',
                'report_extended_payment_group',
                'l10n_ar_account_withholding',
                'web_ir_actions_act_multi'
                ],
    # always loaded
    'data': [
        'reports/certificado_de_retencion_report.xml',        
        'views/account_payment_group_view.xml',
        'views/res_company_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}