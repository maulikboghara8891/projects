from odoo import models, fields,api


class BaseSale(models.Model):
    _inherit = "sale.order"

    description = fields.Char(string="Description")
    is_confirmed_from_wizard = fields.Boolean(default=False)


    def _prepare_invoice(self):

        vals = super()._prepare_invoice()
        vals['description']=self.description
        return vals



    def action_confirm(self):
        if self.is_confirmed_from_wizard:
            return super().action_confirm()

        for line in self.order_line:
            if line.product_id.categ_id in self.company_id.category_ids:
                return {
                    'type': 'ir.actions.act_window',
                    'name': "Confirm",
                    'view_id': self.env.ref('hospital.view_sale_confirm_wizard_form').id,
                    'res_model': 'sale.confirm.wizard',
                    'target': 'new',
                    'view_mode': 'form',
                }
        return super().action_confirm()


