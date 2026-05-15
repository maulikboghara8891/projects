from odoo import models, fields,api
from odoo.exceptions import ValidationError



class CricketTeam(models.Model):
    _name = 'cricket.team'
    _description = 'team'


    tournament_id = fields.Many2one('cricket.tournament')
    team_id=fields.Many2one('team.name')
    group=fields.Selection([
        ('group-a', 'Group-A'),
        ('group-b', 'Group-B'),
        ('group-c', 'Group-C'),
        ('group-d', 'Group-D'),
    ])
    name = fields.Char('short Name', related='team_id.short_name')
    captain_id = fields.Many2one('res.partner')
    total_matches = fields.Integer('Total Matches',)
    total_wins = fields.Integer('Total Wins',)
    lost = fields.Integer('Total lost',)
    tie = fields.Integer('Tie',)
    points = fields.Integer('Points',)
    net_run_rate = fields.Float('Net Run Rate',default=0)
    player_ids = fields.Many2many(
        'res.partner',
        'team_rel',
        'team_id',
        'player_id',
        string='Players'
    )
    coach_ids = fields.Many2many('team.coach',string='coach')


    match_ids = fields.One2many('cricket.matches', 'team_a_id')
    match_b_ids = fields.One2many('cricket.matches', 'team_b_id')





    '''team in 11 players check'''
    # @api.constrains('player_ids')
    # def _check_max_players(self):
    #     for team in self:
    #         if len(team.player_ids) > 11:
    #             raise ValidationError("A team can have **maximum 11 players** only.")
    #         if len(team.player_ids) < 11:
    #             raise ValidationError("A team must have **exactly 11 players**.")

    @api.constrains('player_ids', 'tournament_id')
    def _check_player_unique_per_tournament(self):
        '''player not select in same tournament'''
        for rec in self:
            other_teams = self.search([
                ('tournament_id', '=', rec.tournament_id.id),
                ('id', '!=', rec.id)  # Exclude current team
            ])
            # Collect all players in other teams
            other_players = other_teams.mapped('player_ids')
            overlapping_players = rec.player_ids & other_players
            if overlapping_players:
                names = overlapping_players.mapped('name')
                raise ValidationError(
                    f"This player are already assigned to another team in the same tournament: {names}"
                )

    @api.constrains('coach_ids', 'tournament_id')
    def _check_unique_coach(self):
        '''coach not select in same tournament'''
        for rec in self:
            teams = self.search([
                ('tournament_id', '=', rec.tournament_id.id),
                ('coach_ids', 'in', rec.coach_ids),
                ('id', '!=', rec.id)
            ])
            if teams:
                raise ValidationError("Coach already assigned in this tournament.")

    @api.constrains('tournament_id', 'team_id')
    def _check_unique_team_in_tournament(self):
        '''unique team  create'''
        for rec in self:
            if rec.tournament_id and rec.team_id:
                team = self.search([
                    ('id', '!=', rec.id),
                    ('tournament_id', '=', rec.tournament_id.id),
                    ('team_id', '=', rec.team_id.id)
                ], limit=1)

                if team:
                    raise ValidationError("This team already assigned to this tournament.")