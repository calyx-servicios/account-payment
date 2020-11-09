from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    signature = fields.Binary("Signature", attachment=True,
            help="This field holds the signature used as sign for this contact, limited to 1024x1024px",)