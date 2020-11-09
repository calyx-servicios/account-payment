##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
    _inherit = "account.payment"

    withholding_alicuot = fields.Float(string='Percentage Retention')


class AccountPaymentGroup(models.Model):
    _inherit = "account.payment.group"

    @api.multi
    def payment_print(self):
        _logger.debug('=======AccountPaymentGroup======')
        self.ensure_one()
        self.sent = True
        
        if self.partner_type == 'supplier':
            _logger.debug('=====supplier print')
            self = self.with_context(
                active_model=self._name, active_id=self.id, active_ids=self.ids)
            actions = []
            actions.append(self.env['ir.actions.report'].get_report(self).report_action(
                self))
            for pay in self.payment_ids:
                    if pay.payment_method_code == 'withholding':
                        #actions.append(self.env['ir.actions.report'].get_report(pay).report_action(pay))
                        actions.append(self.env['ir.actions.report']._get_report_from_name('certificado_de_retencion_report_copy').report_action(pay))
            
            return {
                    'type': 'ir.actions.act_multi',
                    'actions': actions
                }
        else:
            _logger.debug('=====customer print')
            return super(AccountPaymentGroup, self).payment_print()