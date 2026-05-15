from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sale_order = fields.Boolean(string='Sale Order', default=False)

    def action_reorder(self):
        current_order_id = self.env.context.get('active_id')
        current_order = self.env['sale.order'].browse(current_order_id)

        for line in self:
            line.env['sale.order.line'].create(
                {
                    'order_id': current_order.id,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'price_subtotal': line.price_subtotal,
                })

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': current_order.id,
                'view_mode': 'form',
                'target': 'current',
            }
