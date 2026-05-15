from odoo import models, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def set_sale(self):
        for record in self:
            if record.state == 'sale':
                raise ValidationError('state is already set')
            else:
                record.state = 'sale'
