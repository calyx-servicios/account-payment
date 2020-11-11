from odoo import models, fields, api

class account_abstract_payment(models.AbstractModel):
    _inherit = "account.abstract.payment"

    @api.one
    @api.constrains("amount")
    def _check_amount(self):
        self.amount        
            