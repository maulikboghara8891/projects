from odoo import fields, models
import json

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    category_ids = fields.Many2many(
        related='company_id.category_ids',
        string="Categories",
        readonly=False
    )
