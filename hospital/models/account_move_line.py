from odoo import models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    no = fields.Integer(string='Number')