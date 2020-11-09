# coding: utf-8
from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    rg2682_type = fields.Selection(
        [('eng', 'Engineering'), ('arch', 'Architecture')],
        string="RG2682 Type"
    )

    # We update the field dynamically
    @api.onchange('tax_withholding_id')
    def _onchange_amount(self):
        self.communication = self.tax_withholding_id.retention_legend

class AccountTax(models.Model):
    _inherit = "account.tax"

    retention_legend = fields.Char(string='Retention Legend')