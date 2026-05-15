from odoo import models,fields,api
from unicodedata import category


class SaleConfirmWizard(models.TransientModel):
    _name = 'sale.confirm.wizard'

    message = fields.Char(string="Message")

    def action_yes(self):
        sale_order = self.env['sale.order'].browse(self.env.context.get('active_id'))

        sale_order.is_confirmed_from_wizard = True
        sale_order.action_confirm()






    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        order = self.env['sale.order'].browse(self.env.context.get('active_id'))
        list=[]

        for line in order.order_line:
            if line.product_id.categ_id in order.company_id.category_ids:
                list.append(line.product_id.name)

        names = order.order_line.mapped('product_id.name')

        res['message'] = "Products:\n" + "\n".join(list)+" same category"

        return res