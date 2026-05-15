from odoo import models, fields,api


class AssignmentRule(models.Model):
    _name='assignment.rule'
    _rec_name = 'assign_role'

    assign_role = fields.Selection([
        ('country', 'Country'),
        ('expected_revenue', 'Expected Revenue')
        ])
    country_id = fields.Many2one('res.country',string='Country')
    revenue_val = fields.Float('Revenue')
    score = fields.Integer('Score')