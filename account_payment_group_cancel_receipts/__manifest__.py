# -*- coding: utf-8 -*-
{
    'name': "Account Payment Group Cancel Receipts",

    'summary': """
        Adds permision on users to disable client receipt cancelation""",

    'description': """
        
    """,

    'author': "Calyx",
    'website': "http://www.calyxservicios.com.ar",

    'category': 'Account',
    'version': '11.0.1.0.0',
    'depends': [
                'base',
                'account_payment_group',
    ],
    'data': [
        'security/security.xml',
        'views/account_payment_group_view.xml'
    ],

}
