from odoo import models, fields,api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    description = fields.Char(string="Description")


