from odoo import models, fields,api


class AutoAssignment(models.Model):
    _name = 'auto.assignment'
    _rec_name = 'user_id'

    user_id =fields.Many2one('res.users')
    min_score = fields.Integer(string='Minimum score')
    country_id = fields.Many2one('res.country')