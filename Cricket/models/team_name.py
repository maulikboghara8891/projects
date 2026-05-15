from odoo import models, fields,api
from odoo.exceptions import ValidationError

class TeamName(models.Model):
    _name = "team.name"
    _description = "Team Name"
    _rec_name="short_name"

    name = fields.Char("Team Name")
    short_name = fields.Char("Short Name")
    city = fields.Char("City")


    @api.constrains('name')
    def _check_unique_name(self):
        for rec in self:
            if rec.name:
                team = self.search([
                    ('id', '!=', rec.id),
                    ('name', '= ilike', rec.name)
                ], limit=1)

                if team:
                    raise ValidationError("Team name must be unique!")