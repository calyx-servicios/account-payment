# coding: utf-8
from odoo import models, fields, api


class PaymentReportWizard(models.TransientModel):
    _name = 'payment.group.report.wizard'

    payment_ids = fields.Many2many('account.payment.group', string='Payments')

    @api.model
    def default_get(self, field_names):
        defaults = super().default_get(field_names)
        selected_ids = self.env.context['active_ids']
        defaults['payment_ids'] = selected_ids
        return defaults

    @api.multi
    def generate_xls_report(self):
        self.ensure_one()
        data = self.read()[0]
        report = self.env.ref(
            'account_payment_group_xlsx_report.payment_group_report_action')
        return report.report_action(self, data=data)
