from odoo import models, fields,api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    no=fields.Integer(string="Number")

    def _prepare_procurement_values(self,):
        self.ensure_one()
        values=super()._prepare_procurement_values()
        values.update({
                        'no' : self.no,
                        'description': self.order_id.description,
                        "sale_line_id": self.id
                    })
        return values

    def _prepare_invoice_line(self, **optional_values):
        '''invoice in line value'''
        vals=super()._prepare_invoice_line(**optional_values)
        vals.update({'no':self.no})
        return vals
