##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)



class AccountPaymentGroup(models.Model):
    _inherit = "account.payment.group"

    @api.multi
    def _compute_matched_move_line_ids(self):
        super(AccountPaymentGroup, self)._compute_matched_move_line_ids()
        for rec in self:
            lines= rec.matched_move_line_ids
            payment_lines = rec.payment_ids.mapped('move_line_ids')
            for line in rec.matched_move_line_ids:
                if line.full_reconcile_id:
                    for reconcile in line.full_reconcile_id.reconciled_line_ids:
                        if reconcile not in lines:
                            lines|= reconcile
            lines = lines-payment_lines
            rec.matched_move_line_ids = lines

    # @api.multi
    # def _compute_matched_move_line_ids(self):
    #     """
    #     Lar partial reconcile vinculan dos apuntes con credit_move_id y
    #     debit_move_id.
    #     Buscamos primeros todas las que tienen en credit_move_id algun apunte
    #     de los que se genero con un pago, etnonces la contrapartida
    #     (debit_move_id), son cosas que se pagaron con este pago. Repetimos
    #     al revz (debit_move_id vs credit_move_id)
    #     """
    #     for rec in self:
    #         lines = rec.move_line_ids.browse()
    #         # not sure why but self.move_line_ids dont work the same way
    #         payment_lines = rec.payment_ids.mapped('move_line_ids')

    #         reconciles = rec.env['account.partial.reconcile'].search([
    #             ('credit_move_id', 'in', payment_lines.ids)])
    #         lines |= reconciles.mapped('debit_move_id')

    #         reconciles = rec.env['account.partial.reconcile'].search([
    #             ('debit_move_id', 'in', payment_lines.ids)])
    #         lines |= reconciles.mapped('credit_move_id')

    #         rec.matched_move_line_ids = lines - payment_lines