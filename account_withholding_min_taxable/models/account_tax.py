from odoo.exceptions import UserError, ValidationError
from ast import literal_eval
from odoo import models, _

class AccountTax(models.Model):
    _inherit = "account.tax"

    def create_payment_withholdings(self, payment_group):
        for tax in self.filtered(lambda x: x.withholding_type != 'none'):
            payment_withholding = self.env[
                'account.payment'].search([
                    ('payment_group_id', '=', payment_group.id),
                    ('tax_withholding_id', '=', tax.id),
                    ('automatic', '=', True),
                ], limit=1)
            if (
                    tax.withholding_user_error_message and
                    tax.withholding_user_error_domain):
                try:
                    domain = literal_eval(tax.withholding_user_error_domain)
                except Exception as e:
                    raise ValidationError(_(
                        'Could not eval rule domain "%s".\n'
                        'This is what we get:\n%s' % (
                            tax.withholding_user_error_domain, e)))
                domain.append(('id', '=', payment_group.id))
                if payment_group.search(domain):
                    raise ValidationError(tax.withholding_user_error_message)
            vals = tax.get_withholding_vals(payment_group)
            currency = payment_group.currency_id
            period_withholding_amount = currency.round(vals.get(
                'period_withholding_amount', 0.0))
            previous_withholding_amount = currency.round(vals.get(
                'previous_withholding_amount'))
            computed_withholding_amount = max(0, (
                period_withholding_amount - previous_withholding_amount))
            if not computed_withholding_amount:
                if payment_withholding:
                    payment_withholding.unlink()
                continue
            vals['withholding_base_amount'] = vals.get(
                'withholdable_advanced_amount') + vals.get(
                'withholdable_invoiced_amount')
            vals['amount'] = computed_withholding_amount
            vals.pop('comment')
            if computed_withholding_amount >= tax.withholding_non_taxable_minimum:
                vals['computed_withholding_amount'] = computed_withholding_amount
                if payment_withholding:
                    payment_withholding.write(vals)
                else:
                    payment_method = self.env.ref(
                        'account_withholding.'
                        'account_payment_method_out_withholding')
                    journal = self.env['account.journal'].search([
                        ('company_id', '=', tax.company_id.id),
                        ('outbound_payment_method_ids', '=', payment_method.id),
                        ('type', 'in', ['cash', 'bank']),
                    ], limit=1)
                    if not journal:
                        raise UserError(_(
                            'No journal for withholdings found on company %s') % (
                            tax.company_id.name))
                    vals['journal_id'] = journal.id
                    vals['payment_method_id'] = payment_method.id
                    vals['payment_type'] = 'outbound'
                    vals['partner_type'] = payment_group.partner_type
                    vals['partner_id'] = payment_group.partner_id.id
                    payment_withholding = payment_withholding.create(vals)
        return True
