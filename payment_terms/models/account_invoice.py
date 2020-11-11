# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.base.res.res_partner import WARNING_MESSAGE, WARNING_HELP
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    postpone = fields.Boolean(
        default=False, string='Postpone Due Date', help='Postpone Due Date a Month')

    check_plan = fields.Boolean(compute='_get_payment_term_plan')

    @api.one
    @api.depends('payment_term_id')
    def _get_payment_term_plan(self):
        if self.payment_term_id and self.payment_term_id.plan:
            self.check_plan  = True
        else:
            self.check_plan  = False


    @api.onchange('payment_term_id', 'date_invoice', 'postpone')
    def _onchange_payment_term_date_invoice(self):
        if self.payment_term_id and self.payment_term_id.plan:
            date_invoice = self.date_invoice
            if not date_invoice:
                date_invoice = fields.Date.context_today(self)
            if self.postpone:
                next_date = fields.Date.from_string(date_invoice)
                next_date += relativedelta(months=2)
                date_invoice = fields.Date.to_string(next_date)
            if self.payment_term_id:
                pterm = self.payment_term_id
                pterm_list = pterm.with_context(currency_id=self.company_id.currency_id.id).compute(
                    value=1, date_ref=date_invoice)[0]
                self.date_due = max(line[0] for line in pterm_list)
            elif self.date_due and (date_invoice > self.date_due):
                self.date_due = date_invoice
        else:
            super(AccountInvoice, self)._onchange_payment_term_date_invoice()

    @api.multi
    def action_invoice_open(self):
        self.env.context = dict(self.env.context)
        self.env.context.update({'postpone': self.postpone})
        super(AccountInvoice, self).action_invoice_open()

    

class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    plan = fields.Boolean(default=False, help="This is a plan payment term")
    plan_day = fields.Integer('Day of Month')
    plan_split = fields.Integer('Plan Split')

    @api.one
    def compute(self, value, date_ref=False):
        ctx=self._context
        date_ref = date_ref or fields.Date.today()
        
        amount = value
        result = []
        if self.env.context.get('currency_id'):
            currency = self.env['res.currency'].browse(
                self.env.context['currency_id'])
        else:
            currency = self.env.user.company_id.currency_id
        if not self.plan:
            for line in self.line_ids:
                if line.value == 'fixed':
                    amt = currency.round(line.value_amount)
                elif line.value == 'percent':
                    amt = currency.round(value * (line.value_amount / 100.0))
                elif line.value == 'balance':
                    amt = currency.round(amount)
                if amt:
                    next_date = fields.Date.from_string(date_ref)
                    if line.option == 'day_after_invoice_date':
                        next_date += relativedelta(days=line.days)
                    elif line.option == 'fix_day_following_month':
                        # Getting 1st of next month
                        next_first_date = next_date + \
                            relativedelta(day=1, months=1)
                        next_date = next_first_date + \
                            relativedelta(days=line.days - 1)
                    elif line.option == 'last_day_following_month':
                        # Getting last day of next month
                        next_date += relativedelta(day=31, months=1)
                    elif line.option == 'last_day_current_month':
                        # Getting last day of next month
                        next_date += relativedelta(day=31, months=0)
                    result.append((fields.Date.to_string(next_date), amt))
                    amount -= amt

        else:
            # date_ref = fields.Date.today()
            if self.env.context.get('postpone'):
                next_date = fields.Date.from_string(date_ref)
                next_date += relativedelta(day=self.plan_day, months=1)
                date_ref=fields.Date.to_string(next_date)
            for i in range(self.plan_split):
                

                next_date = fields.Date.from_string(date_ref)
                amt = currency.round(value / self.plan_split)
                next_date += relativedelta(day=self.plan_day, months=i+1)
                if i == self.plan_split-1:
                    amount = sum(amt for _, amt in result)
                    dist = currency.round(value - amount)
                    amt = dist
                result.append((fields.Date.to_string(next_date), amt))
        
        return result
