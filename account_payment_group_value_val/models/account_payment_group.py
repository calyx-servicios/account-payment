# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, api, _
from odoo.exceptions import UserError


class AccountPaymentGroup(models.Model):
    _inherit = "account.payment.group"

    @api.multi
    def post(self):
        validation = self._get_account_payment_validation()
        error_string = ""
        if self.partner_type == "customer":
            error_string = _(
                "You cannot validate a partner anticipate with amount in 0.0"
            )
        elif self.partner_type == "supplier":
            error_string = _(
                "You cannot validate a supplier payment with amount in 0.0"
            )

        if validation:
            if self.payments_amount == 0.0:
                raise UserError(error_string)

        return super(AccountPaymentGroup, self).post()

    @api.multi
    def _get_account_payment_validation(self):

        icpsudo = self.env["ir.config_parameter"].sudo()
        validation = icpsudo.get_param(
            "account_payment_group_value_val.account_payment_validation"
        )
        return validation
