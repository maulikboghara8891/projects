from odoo import models, fields,api
# from datetime import date
# from odoo.exceptions import ValidationError


class TeamCoach(models.Model):
    _name = 'team.coach'
    _description = 'Team.Coach'


    name = fields.Char(string="Coach Name", required=True)
    phone = fields.Char(string="Phone")
    age = fields.Integer(string="Age")
    experience = fields.Integer(string="Experience (Years)")
    specialization = fields.Selection([
        ('batting', 'Batting Coach'),
        ('bowling', 'Bowling Coach'),
        ('all_rounder', 'All rounder')
    ], string="Coach Type")
    team_ids = fields.Many2many('cricket.team', string="Teams")


