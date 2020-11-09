# © 2020 Calyx Servicios S.A.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, _
from odoo.exceptions import RedirectWarning


class AccountPaymentGroup(models.Model):
    _inherit = "account.payment.group"

    # Fields to show the sum of paid invoices with SUSS products lines
    works_eng = fields.Monetary(string='Engineering Works', compute='_compute_works_eng', store=True)
    works_arch = fields.Monetary(string='Architecture Works', compute='_compute_works_arch', store=True)
    # Fields to mark when an account payment group has SUSS lines
    suss_lines_eng = fields.Boolean(string='SUSS Lines Eng checker')
    suss_lines_arch = fields.Boolean(string='SUSS Lines Arch checker')
    # Fields to save the last SUSS Retention
    suss_last_eng = fields.Monetary(string='Last eng ret to save')
    suss_last_arch = fields.Monetary(string='Last arch ret to save')
    # Fields to show the last SUSS Retention in the UI before the new value
    suss_last_eng_view = fields.Monetary(string='Last Engineering SUSS Retention')
    suss_last_arch_view = fields.Monetary(string='Last Architecture SUSS Retention')
    # Field to show the SUSS Page in Account Payment Form view in case the Partner has > 0 in any SUSS Product Type
    show_suss = fields.Boolean(compute='_compute_show_suss', store=True, default=lambda self: False)

    @api.multi
    def compute_withholdings(self):
        result = super(AccountPaymentGroup, self).compute_withholdings()
        for payment_group in self:
            acc_eng_upd = 0
            acc_arch_upd = 0
            for debt_line in payment_group.debt_move_line_ids:
                for debt_invoice in debt_line.invoice_id:
                    for line_invoice in debt_invoice.invoice_line_ids:
                        if line_invoice.product_id.rg2682_type == 'eng':
                            acc_eng_upd += line_invoice.price_subtotal
                        elif line_invoice.product_id.rg2682_type == 'arch':
                            acc_arch_upd += line_invoice.price_subtotal

            new_eng_amount = self.get_accumulate('eng') + acc_eng_upd
            payment_group.write({'works_eng': new_eng_amount})

            new_arch_amount = self.get_accumulate('arch') + acc_arch_upd
            payment_group.write({'works_arch': new_arch_amount})

            if payment_group.works_eng >= 1500000:
                # SUSS Calculation
                # Check if older retention exists
                amount_calculation = payment_group.works_eng * 0.012

                last_retention = self.env['account.payment.group'].search(
                    [('suss_lines_eng', '=', True), ('payment_date', '>=', self.payment_date),
                     ('payment_date', '<=', self.payment_date), ('id', '!=', self.id),
                     ('state', '=', 'posted'), ('partner_id', '=', self.partner_id.id)],
                    order='id desc', limit=1)

                if last_retention:
                    amount_calculation = amount_calculation - last_retention.suss_last_eng
                    self.suss_last_eng_view = last_retention.suss_last_eng
                    if amount_calculation > 0:
                        self.suss_last_eng = last_retention.suss_last_eng + amount_calculation
                else:
                    self.suss_last_eng = amount_calculation

                # Check if we already have a 'eng' retention line
                for payment_line in payment_group.payment_ids:
                    if payment_line.rg2682_type == 'eng':
                        payment_line.amount = amount_calculation
                        break
                # If we didn't find one
                else:
                    if amount_calculation > 0:
                        journal = self.env['account.journal'].search(
                            [('type', '=', 'cash'), ('company_id', '=', self.company_id.id),
                             ('code', '=', 'CSH3'), ('name', 'ilike', 'Reten')]
                        ).id

                        tax = self.env['account.tax'].with_context(type='cash').search(
                            [('id', '=', self.env.ref('account_payment_suss.with_rg2682').id)]
                        )

                        if not tax.account_id or not tax.refund_account_id:
                            action = self.env.ref('account_withholding.action_withholding_tax_form')
                            msg = _('It seems %s has no Accounts assigned.\n') % tax.name
                            raise RedirectWarning(msg, action.id, _('Go to Withholding Taxes'))

                        vals = {
                            'state': 'draft',
                            'journal_id': journal,
                            'tax_withholding_id': tax.id,
                            'withholding_base_amount': payment_group.works_eng,
                            'amount': amount_calculation,
                            'payment_date': payment_group.payment_date,
                            'partner_id': payment_group.partner_id.id,
                            'partner_type': payment_group.partner_type,
                            'payment_group_id': payment_group.id,
                            'communication': _('Engineering ') + tax.name,
                            'payment_type': 'outbound',
                            'payment_method_id': 8,
                            'rg2682_type': 'eng',
                            'boolean_check_payment_group': True,
                        }
                        # Update field in case there is a legend configured for this withholding tax
                        if tax.retention_legend:
                            vals["communication"] = tax.retention_legend

                        self.env['account.payment'].create(vals)
                        self.suss_lines_eng = True

            if payment_group.works_arch >= 1500000:
                # SUSS Calculation
                # Check if older retention exists
                amount_calculation = payment_group.works_arch * 0.025

                last_retention = self.env['account.payment.group'].search(
                    [('suss_lines_arch', '=', True), ('payment_date', '>=', self.payment_date),
                     ('payment_date', '<=', self.payment_date), ('id', '!=', self.id),
                     ('state', '=', 'posted'), ('partner_id', '=', self.partner_id.id)],
                    order='id desc', limit=1)

                if last_retention:
                    amount_calculation = amount_calculation - last_retention.suss_last_arch
                    self.suss_last_arch_view = last_retention.suss_last_arch
                    if amount_calculation > 0:
                        self.suss_last_arch = last_retention.suss_last_arch + amount_calculation
                else:
                    self.suss_last_arch = amount_calculation

                # Check if we already have a 'eng' retention line
                for payment_line in payment_group.payment_ids:
                    if payment_line.rg2682_type == 'arch':
                        payment_line.amount = amount_calculation
                        break
                # If we didn't find one
                else:
                    if amount_calculation > 0:
                        journal = self.env['account.journal'].search(
                            [('type', '=', 'cash'), ('company_id', '=', self.company_id.id),
                             ('code', '=', 'CSH3'), ('name', 'ilike', 'Reten')]
                        ).id

                        tax = self.env['account.tax'].with_context(type='cash').search(
                            [('id', '=', self.env.ref('account_payment_suss.with_rg2682').id)]
                        )

                        if not tax.account_id or not tax.refund_account_id:
                            action = self.env.ref('account_withholding.action_withholding_tax_form')
                            msg = _('It seems %s has no Accounts assigned.\n') % tax.name
                            raise RedirectWarning(msg, action.id, _('Go to Withholding Taxes'))

                        vals = {
                            'state': 'draft',
                            'journal_id': journal,
                            'tax_withholding_id': tax.id,
                            'withholding_base_amount': payment_group.works_arch,
                            'amount': amount_calculation,
                            'payment_date': payment_group.payment_date,
                            'partner_id': payment_group.partner_id.id,
                            'partner_type': payment_group.partner_type,
                            'payment_group_id': payment_group.id,
                            'communication': _('Architecture ') + tax.name,
                            'payment_type': 'outbound',
                            'payment_method_id': 8,
                            'rg2682_type': 'arch',
                            'boolean_check_payment_group': True,
                        }
                        # Update field in case there is a legend configured for this withholding tax
                        if tax.retention_legend:
                            vals["communication"] = tax.retention_legend

                        self.env['account.payment'].create(vals)
                        self.suss_lines_arch = True

        return result

    def get_accumulate(self, concept_type):
        for payment_group in self:
            partner_invoices = payment_group.env['account.invoice'].search([
                ('partner_id', '=', payment_group.partner_id.id),
                ('type', '=', 'in_invoice'),
                ('state', '=', 'paid')
            ])

            partner_invoices = partner_invoices.filtered(
                lambda invoice_obj: invoice_obj.date and invoice_obj.date[:4] == payment_group.payment_date[:4])

            acc = 0
            for invoice in partner_invoices:
                for line in invoice.invoice_line_ids:
                    if line.product_id.rg2682_type == concept_type:
                        acc += line.price_subtotal

            return acc

    @api.one
    @api.depends('partner_id', 'payment_date')
    def _compute_works_eng(self):
        acc_eng = self.get_accumulate('eng')
        self.works_eng = acc_eng

    @api.one
    @api.depends('partner_id', 'payment_date')
    def _compute_works_arch(self):
        acc_arch = self.get_accumulate('arch')
        self.works_arch = acc_arch

    @api.one
    @api.depends('works_eng', 'works_arch')
    def _compute_show_suss(self):
        if self.works_arch or self.works_eng:
            self.show_suss = True
