from odoo import models, fields, _

ALIQUOT_GI_LOCAL = 0.025
ALIQUOT_GI_MULTILATERAL = 0.01

ALIQUOT_HL_LOCAL = 0.2
ALIQUOT_HL_MULTILATERAL = 0.5


def get_vals_gi_san_juan(
    env, payment_group: models.Model, gi_type: str, vals: dict
) -> dict:
    """Calculate the value for the San Juan Home Gross Income withholding.

    Args:
        env: Odoo's environment.
        payment_group (models.Model): account.payment.group record.
        gi_type (str): partner_id.l10n_ar_gross_income_type value.
        vals (dict): values to be updated, then used to create the withholding payment line.

    Returns:
        dict: values updated (or not), then used to create the withholding payment line.
    """
    aliquot = ALIQUOT_GI_LOCAL if gi_type == "local" else ALIQUOT_GI_MULTILATERAL
    resp_type = payment_group.partner_id.l10n_ar_afip_responsibility_type_id

    if resp_type == env.ref("l10n_ar.res_IVARI"):
        invoice_untaxed_amount = amount = payment_group.selected_debt_untaxed
        vals["period_withholding_amount"] = invoice_untaxed_amount * aliquot
    else:
        invoice_amount = amount = payment_group.selected_debt
        vals["period_withholding_amount"] = invoice_amount * aliquot

    gi_type_prefix = _("taxpayer") if gi_type == "local" else _("agreement")
    invoice_amount_type = (
        _("net") if resp_type == env.ref("l10n_ar.res_IVARI") else _("total")
    )

    vals["communication"] = (
        f"{resp_type.display_name} ({_('amount of invoice')} {invoice_amount_type} "
        f"- ${amount}) {_('and')} "
        f"{gi_type_prefix.capitalize()} {gi_type.capitalize()} - %{aliquot * 100}"
    )

    return vals


def get_vals_gi_san_juan_home_lot(
    payment_group: models.Model, gi_type: str, vals: dict
) -> dict:
    """Calculate the value for the San Juan Home Lot withholding.

    Args:
        payment_group (models.Model): account.payment.group record.
        gi_type (str): partner_id.l10n_ar_gross_income_type value.
        vals (dict): values to be updated, then used to create the withholding payment line.

    Returns:
        dict: values updated (or not), then used to create the withholding payment line.
    """
    aliquot = ALIQUOT_HL_LOCAL if gi_type == "local" else ALIQUOT_HL_MULTILATERAL

    # We need a previously created San Juan Gross Income withholding to get the amount
    gi_san_juan_line = payment_group.mapped("payment_ids").filtered(
        lambda x: x.tax_withholding_id.withholding_type == "specific_case"
        and x.tax_withholding_id.withholding_type_specific_case == "applied_gi_san_juan"
    )
    if not gi_san_juan_line:
        return vals

    vals["period_withholding_amount"] = gi_san_juan_line.amount * aliquot

    gi_type_prefix = _("taxpayer") if gi_type == "local" else _("agreement")
    vals["communication"] = (
        f"{gi_type_prefix.capitalize()} {gi_type.capitalize()} - "
        f"%{aliquot * 100} {_('of San Juan Gross Income withholding')} (${gi_san_juan_line.amount})"
    )
    return vals


class AccountTax(models.Model):
    _inherit = "account.tax"

    withholding_type_specific_case = fields.Selection(
        selection_add=[
            (
                "applied_gi_san_juan",
                "Applied Gross Income San Juan",
            ),
            (
                "applied_gi_san_juan_home_lot",
                "Applied Gross Income San Juan Home Lot",
            ),
        ]
    )

    def get_withholding_vals(self, payment_group: models.Model) -> dict:
        """We inherit this method to add the specific case withholding
        only for partners from San Juan state.

        Args:
            payment_group (models.Model): account.payment.group record.

        Returns:
            dict: values used to create the withholding payment line.
        """
        vals = super().get_withholding_vals(payment_group)

        # Check if the partner is from San Juan (Argentina) state.
        if payment_group.partner_id.state_id != self.env.ref("base.state_ar_j"):
            return vals
        # Check if the partner has 'exempt' as Gross Income type.
        gi_type = payment_group.partner_id.l10n_ar_gross_income_type
        if gi_type == "exempt":
            return vals

        w_type = self.withholding_type
        w_type_case = self.withholding_type_specific_case

        if w_type == "specific_case":
            if w_type_case == "applied_gi_san_juan":
                vals = get_vals_gi_san_juan(self.env, payment_group, gi_type, vals)
            if w_type_case == "applied_gi_san_juan_home_lot":
                vals = get_vals_gi_san_juan_home_lot(payment_group, gi_type, vals)

        return vals
