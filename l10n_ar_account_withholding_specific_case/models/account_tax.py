from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountTax(models.Model):
    _inherit = "account.tax"

    withholding_type = fields.Selection(
        selection_add=[
            ("specific_case", "Specific Case"),
        ]
    )

    withholding_type_specific_case = fields.Selection(
        selection=[
            ("no_case", "No Specific Case"),
        ],
        default="no_case",
    )

    @api.constrains("withholding_type", "withholding_type_specific_case")
    def _check_withholding_type_specific_case(self):
        for rec in self:
            w_type = rec.withholding_type
            case = rec.withholding_type_specific_case
            if w_type == "specific_case" and case in [False, "no_case"]:
                raise ValidationError(
                    _("You must select a Specific Case for this withholding type.")
                )
