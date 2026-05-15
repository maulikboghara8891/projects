from odoo import models, fields,api
# from datetime import date
from odoo.exceptions import ValidationError


class TeamPoints(models.Model):
    _name = 'team.points'
    _description = 'Team.Points'
    _rec_name = 'team_id'

    tournament_id = fields.Many2one('cricket.tournament','tournament ')
    team_id = fields.Many2one('cricket.team','team ')
    matches_played = fields.Integer(related='team_id.total_matches')
    wins = fields.Integer(related='team_id.total_wins')
    losses = fields.Integer(related='team_id.lost')
    ties = fields.Integer(related='team_id.tie')
    points = fields.Integer(related='team_id.points')
    # group = fields.Selection(related='team_id.group')

    @api.constrains('tournament_id', 'team_id')
    def _check_unique_team_in_tournament(self):
        '''unique point table create'''
        for rec in self:
            if rec.tournament_id and rec.team_id:
                existing = self.search([
                    ('id', '!=', rec.id),
                    ('tournament_id', '=', rec.tournament_id.id),
                    ('team_id', '=', rec.team_id.id)
                ], limit=1)

                if existing:
                    raise ValidationError("This point table already added ")


    def action_view_matches(self):
        '''view matches on smart button'''
        return {
            'type': 'ir.actions.act_window',
            'name': 'Matches',
            'res_model': 'cricket.matches',
            'view_mode': 'list,form',
            'domain': ['&',
                            '|',
                                ('team_a_id', '=', self.team_id.id),
                                ('team_b_id', '=', self.team_id.id),
                            ('status','=','finished')]
        }

