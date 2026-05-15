from odoo import models, fields,api


class AccountMove(models.Model):
    _inherit = "account.move"

    description = fields.Char(string="Description Done")