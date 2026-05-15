from odoo import models, fields,api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    description = fields.Char(string="Description")

    def _prepare_picking(self):
        vals=super()._prepare_picking()
        vals.update({
            'description':self.description,
        })
        return vals

    def button_confirm(self):
        res = super().button_confirm()
        for order in self.picking_ids.move_ids:
            order._action_assign()
            order.picking_id.button_validate()
        return res
