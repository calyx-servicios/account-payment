from odoo import models,fields,api,_

class AccountPaymentGroup(models.Model):
    _inherit = 'account.payment.group'

    payments_amount = fields.Monetary(
        compute='_compute_payments_amount',
        string='Amount',
        track_visibility='always',
        store=True,
    )

    