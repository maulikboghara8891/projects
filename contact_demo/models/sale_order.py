from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    minimum = fields.Float(string='Minimum Price', compute="_compute_min")
    result = fields.Char(string="Result", compute="_compute_result")
    sale_order_ids = fields.One2many('sale.order.line', 'order_id', compute='_compute_sale_order_ids',
                                     string="Sales Orders")

    @api.depends('partner_id')
    def _compute_sale_order_ids(self):
        for rec in self:
            '''select partner_id show all sale orders'''
            rec.sale_order_ids = self.env['sale.order.line'].search([
                ('order_id.partner_id', '=', rec.partner_id.id),
                ('order_id', '!=', self.id),
            ])

    def action_reorder(self):
        for line in self.sale_order_ids:
            if line.sale_order:
                line.env['sale.order.line'].create(
                    {
                        'order_id': self.id,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'price_subtotal': line.price_subtotal,
                    })
                line.sale_order = False
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_done(self):
        return self._create_invoices()

    @api.depends('partner_id')
    def _compute_min(self):
        self.minimum = self.partner_id.minimum

    @api.depends('amount_total')
    def _compute_result(self):
        if self.minimum <= self.amount_total:
            self.result = "max"
        else:
            self.result = "min"

    @api.depends('partner_id')
    def _compute_partner_shipping_id(self):
        '''set confirm child '''
        super()._compute_partner_shipping_id()
        for rec in self:
            if rec.partner_id:
                child = self.env['res.partner'].search([
                    ('id', 'child_of', self.partner_id.id),
                    ('confirm', '=', True)
                ], limit=1)

                if child:
                    self.partner_shipping_id = child.id


