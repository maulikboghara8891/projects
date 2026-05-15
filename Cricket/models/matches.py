from odoo import models, fields,api
from odoo.exceptions import ValidationError
from datetime import date

class CricketMatches(models.Model):
    _name = 'cricket.matches'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Cricket Matches'


    tournament_id = fields.Many2one('cricket.tournament')
    team_a_id = fields.Many2one('cricket.team')
    team_b_id = fields.Many2one('cricket.team')
    name = fields.Char('Teams', compute='_compute_name')
    match_date = fields.Date('Date')
    stadium_id = fields.Many2one('cricket.venue')
    street = fields.Char(related='stadium_id.street')
    city=fields.Char(related='stadium_id.city')
    state=fields.Char(related='stadium_id.state')
    country=fields.Char(related='stadium_id.country')
    status = fields.Selection([
        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('finished', 'Finished'),
    ],'status',default='upcoming')
    overs=fields.Integer('overs')
    toss_winer_id=fields.Many2one('cricket.team')
    toss_decision=fields.Selection([
        ('batting', 'Batting'),
        ('bowling', 'Bowling')
    ])
    team_a_wickets = fields.Integer(string="Team A Wickets")
    team_b_wickets = fields.Integer(string="Team B Wickets")
    win=fields.Char('Winner',store=True )
    team_a_runs = fields.Integer('Team A Runs', default=0,tracking=True)
    team_b_runs = fields.Integer('Team B Runs', default=0,tracking=True)
    # team_a_line = fields.One2many(
    #     "match.player.line",
    #     "match_id",
    #     string="Players",
    # )
    # team_b_line = fields.One2many(
    #     "match.player.line",
    #     "match_id",
    #     string="Players",
    # )
    #
    # @api.onchange("team_a_id")
    # def _onchange_team_a(self):
    #     if self.team_a_id:
    #         lines = []
    #         for player in self.team_a_id.player_ids:
    #             lines.append((0, 0, {
    #                 "team_id": self.team_a_id.id,
    #                 "player_id": player.id,
    #             }))
    #         self.team_a_line = lines
    #
    # @api.onchange("team_b_id")
    # def _onchange_team_b(self):
    #     if self.team_b_id:
    #         lines = []
    #         for player in self.team_b_id.player_ids:
    #             lines.append((0, 0, {
    #                 "team_id": self.team_b_id.id,
    #                 "player_id": player.id,
    #
    #             }))
    #         self.team_a_line = lines

    @api.depends('team_a_id', 'team_b_id')
    def _compute_name(self):
        '''team name create A vs B'''
        for rec in self:
            if rec.team_a_id and rec.team_b_id:
                rec.name = f"{rec.team_a_id.name} vs {rec.team_b_id.name}"
            else:
                rec.name =False

    @api.depends('match_date')
    def update_status(self):
        '''cron method for updating tournament status'''

        today = date.today()
        matches = self.search([('match_date', '=', today)])
        for rec in matches:
            rec.status = 'live'

    @api.constrains('match_date','team_a_id','team_b_id')
    def _check_tournament_date(self):
        '''check tournament  date and that on match fix'''
        for rec in self:
            if rec.tournament_id.start_date > rec.match_date or rec.tournament_id.end_date < rec.match_date:
                raise ValidationError("please date verify tournament dates.")
            domain = [
                ('match_date', '=', rec.match_date),
                ('id', '!=', rec.id),
                '|',
                ('team_a_id', 'in', [rec.team_a_id.id, rec.team_b_id.id]),
                ('team_b_id', 'in', [rec.team_a_id.id, rec.team_b_id.id])
            ]
            match = self.search(domain)
            if match:
                team_names = ", ".join(
                    match.mapped('team_a_id.name') + match.mapped('team_b_id.name')
                )
                raise ValidationError(f"{team_names} team already has a match on this date.")


    def status_live(self):
            '''check date tournament , today date then live on button'''
            for record in self:
                today = date.today()
                if record.match_date != today:
                    raise ValidationError("Match date is not today Cannot set Live.")
                record.status="live"



    # @api.depends('team_a_player_ids.runs','team_a_extra_runs')
    # def _compute_team_a_total_runs(self):
    #     '''team a total runs'''
    #     for match in self:
    #         total = 0
    #         for player in match.team_a_player_ids:
    #             total += player.runs
    #         match.team_a_runs = total+ match.team_a_extra_runs
    #
    # @api.depends('team_b_player_ids.runs', 'team_b_extra_runs')
    # def _compute_team_b_total_runs(self):
    #     ''' team a total runs'''
    #     for match in self:
    #         total = 0
    #         for player in match.team_b_player_ids:
    #             total += player.runs
    #         match.team_b_runs = total + match.team_b_extra_runs

    def add_run(self):
        ''' button on wizard through run add'''
        return {
            'type': 'ir.actions.act_window',
            'name': "add run",
            'view_id': self.env.ref('Cricket.match_run_wizard_form').id,
            'res_model': 'match.runs.wizard',
            'target': 'new',
            'view_mode': 'form',
        }


    def status_finis(self):
        '''status finished
                match result show
                count matches,won,points  on button'''
        for record in self:
            if not(record.team_a_runs and record.team_b_runs):
                raise ValidationError("please enter runs after finished")
            record.team_a_id.total_matches +=1
            record.team_b_id.total_matches +=1


            for player in record.team_a_id.player_ids | record.team_b_id.player_ids:
                player.matches_played += 1

            if record.team_a_runs > record.team_b_runs:
                record.win = record.team_a_id.name
                record.team_a_id.total_wins +=1
                record.team_a_id.points +=2
                record.team_b_id.lost +=1

            elif record.team_b_runs > record.team_a_runs:
                record.win = record.team_b_id.name
                record.team_b_id.total_wins += 1
                record.team_b_id.points += 2
                record.team_a_id.lost += 1

            elif record.team_a_runs == record.team_b_runs:
                record.win = "Draw"
                record.team_a_id.tie +=1
                record.team_b_id.tie +=1
                record.team_a_id.points +=1
                record.team_b_id.lost +=1
            record.status = 'finished'

