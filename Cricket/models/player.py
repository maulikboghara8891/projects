from odoo import models, fields,_


class CricketPlayer(models.Model):
    _name = 'cricket.player'

    _description = 'Cricket Players'

    name = fields.Char('Name',)
    age = fields.Integer('Age')
    role=fields.Selection([
        ('batsman', 'Batsman'),
        ('bowler', 'Bowler'),
        ('all_rounder', 'All rounder'),
        ('wicket_keeper', 'Wicket keeper')],'Role',)
    matches_played=fields.Integer('Matches played')
    runs=fields.Integer('Runs')
    wickets=fields.Integer('Wickets')
    team_ids = fields.Many2many('cricket.team','player_team_rel','team_id','player_id',string='Teams')



    _player_unique = models.Constraint(
        'unique (name)',
        'already add!',
    )



    def role_change(self):

        for record in self:
             record.role = "bowler"
