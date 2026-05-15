from odoo import models, fields,api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    no=fields.Integer(string='No.')


    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        vals=super()._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        vals['no'] = self.no
        return vals

    def _prepare_purchase_order_line_from_procurement(self, product_id, product_qty, product_uom, location_dest_id,name, origin, company_id, values, po):
        res = super()._prepare_purchase_order_line_from_procurement( product_id, product_qty, product_uom,location_dest_id, name, origin, company_id, values, po)
        sale_line_id = values.get('sale_line_id')
        if sale_line_id:
            sale_line = self.env['sale.order.line'].browse(sale_line_id)
            res['no']=sale_line.no
        return res

