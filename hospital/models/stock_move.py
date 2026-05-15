from odoo import models, fields,api


class StockMove(models.Model):
    _inherit = 'stock.move'

    no = fields.Integer("no")
    description = fields.Char(string="Description")

    def _get_new_picking_values(self):
        '''picking in field value update'''
        vals = super()._get_new_picking_values()
        vals.update({
            'description': self[0].description,
        })
        return vals