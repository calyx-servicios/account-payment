# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    account_payment_validation = fields.Boolean(
        "Validate supplier payment and partner anticipes?",
        default=False,
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        icpsudo = self.env["ir.config_parameter"].sudo()
        validation = icpsudo.get_param(
            "account_payment_group_value_val.account_payment_validation"
        )
        res.update(account_payment_validation=validation)
        return res

    @api.multi
    def set_values(self):
        res = super().set_values()
        self.env["ir.config_parameter"].set_param(
            "account_payment_group_value_val.account_payment_validation",
            self.account_payment_validation,
        )
        return res
