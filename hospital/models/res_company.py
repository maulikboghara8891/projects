from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    category_ids = fields.Many2many(
        "product.category",
        string="Category",
    )
