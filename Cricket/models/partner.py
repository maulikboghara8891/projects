from odoo import models, fields,api

class Partner(models.Model):
    _inherit = 'res.partner'

    age = fields.Integer('Age')
    role = fields.Selection([
        ('batsman', 'Batsman'),
        ('bowler', 'Bowler'),
        ('all_rounder', 'All_rounder'),
        ('wicket_keeper', 'Wicket_keeper')], 'Role')
    matches_played = fields.Integer('Matches played')
    total_runs = fields.Integer('Total runs')
    # runs = fields.Integer('Runs',default=0)
    wickets = fields.Integer('Wickets')
    team_ids = fields.Many2many('cricket.team','team_rel','player_id','team_id',string='Teams')
    # total_teams = fields.Integer('Total teams',compute='_compute_total_teams')

    def role_set_bowler(self):
        '''server action'''
        self.role='bowler'

    # @api.depends('team_ids')
    # def _compute_total_teams(self):
    #     for record in self:
    #         record.total_teams = len(record.team_ids)

    def view_teams(self):
        teams = self.env['cricket.team'].search([
            ('player_ids', 'in', self.id)
        ])

        if len(teams) == 1:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Teams',
                'res_model': 'cricket.team',
                'view_mode': 'form',
                'res_id':teams.id,
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Teams',
                'res_model': 'cricket.team',
                'view_mode': 'list,form',
                'domain': [('id', 'in', teams.ids)],
            }