# coding: utf-8
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.template'

    rg2682_type = fields.Selection(
        [('eng', 'Engineering'), ('arch', 'Architecture')],
        string="RG2682 Type"
    )