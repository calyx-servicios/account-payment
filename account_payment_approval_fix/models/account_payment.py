from odoo import models, fields, _

class AccountPayment(models.Model):
    _inherit = "account.payment"

    def post(self):
        """Overwrites the post() to validate the payment in the 'approved' stage too.
        Currently Odoo allows payment posting only in draft stage.
        """
        AccountMove = self.env['account.move'].with_context(default_type='entry')
        for rec in self:
            validation = rec._check_payment_approval()
            if validation:
                if rec.state not in ('draft', 'approved'):
                    raise UserError(_("Only a draft or approved payment can be posted."))

                if any(inv.state != 'posted' for inv in rec.invoice_ids):
                    raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

                # keep the name in case of a payment reset to draft
                if not rec.name:
                    # Use the right sequence to set the name
                    if rec.payment_type == 'transfer':
                        sequence_code = 'account.payment.transfer'
                    else:
                        if rec.partner_type == 'customer':
                            if rec.payment_type == 'inbound':
                                sequence_code = 'account.payment.customer.invoice'
                            if rec.payment_type == 'outbound':
                                sequence_code = 'account.payment.customer.refund'
                        if rec.partner_type == 'supplier':
                            if rec.payment_type == 'inbound':
                                sequence_code = 'account.payment.supplier.refund'
                            if rec.payment_type == 'outbound':
                                sequence_code = 'account.payment.supplier.invoice'
                    rec.name = self.env['ir.sequence'].next_by_code(sequence_code, sequence_date=rec.payment_date)
                    if not rec.name and rec.payment_type != 'transfer':
                        raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

                moves = AccountMove.create(rec._prepare_payment_moves())
                moves.filtered(lambda move: move.journal_id.post_at != 'bank_rec').post()

                # Update the state / move before performing any reconciliation.
                move_name = self._get_move_name_transfer_separator().join(moves.mapped('name'))
                rec.write({'state': 'posted', 'move_name': move_name})

                if rec.payment_type in ('inbound', 'outbound'):
                    # ==== 'inbound' / 'outbound' ====
                    if rec.invoice_ids:
                        (moves[0] + rec.invoice_ids).line_ids \
                            .filtered(
                            lambda line: not line.reconciled and line.account_id == rec.destination_account_id) \
                            .reconcile()
                elif rec.payment_type == 'transfer':
                    # ==== 'transfer' ====
                    moves.mapped('line_ids') \
                        .filtered(lambda line: line.account_id == rec.company_id.transfer_account_id) \
                        .reconcile()

        return True
