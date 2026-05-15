from odoo import models, fields,api
from datetime import date
from odoo.exceptions import ValidationError

from odoo_19.odoo.odoo.orm.decorators import readonly


class CricketTournament(models.Model):
    _name = 'cricket.tournament'
    _description = 'Cricket Tournament'
    _rec_name = 'tournament'

    tournament= fields.Char('Tournament Name')
    season_date= fields.Date('season date')
    season_year =fields.Char('year',compute='_compute_season_year')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    matches_ids = fields.One2many('cricket.matches', 'tournament_id','Matches')
    team_ids = fields.One2many('cricket.team','tournament_id','Teams')
    status = fields.Selection([
        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('finished', 'Finished'),
    ], 'status',compute='_compute_status')
    total_matches = fields.Integer('Total Matches',compute='_compute_total_matches',default=0)
    total_teams = fields.Integer('Total Teams',readonly=True)



    @api.depends('season_date')
    def _compute_season_year(self):
        '''date on season year'''
        for rec in self:
            rec.season_year = rec.season_date.year if rec.season_date else False

    @api.constrains('end_date')
    def _check_match_date(self):
        '''check end date greater than start date'''
        for rec in self:
            if rec.start_date > rec.end_date:
                raise ValidationError("End date greater than start date")

    @api.depends('start_date', 'end_date')
    def _compute_status(self):
        '''date no set tournament status'''
        today = date.today()
        for rec in self:
            rec.status = 'upcoming'
            if rec.start_date and rec.end_date:
                if today < rec.start_date:
                    rec.status = 'upcoming'
                elif rec.start_date <= today <= rec.end_date:
                    rec.status = 'live'
                elif today > rec.end_date:
                    rec.status = 'finished'

    @api.depends('matches_ids', 'team_ids')
    def _compute_total_matches(self):
        for rec in self:
            '''find total matches,teams'''
            rec.total_matches = len(rec.matches_ids)
            rec.total_teams = len(rec.team_ids)


    def view_matches(self):
        '''view matches on smart button'''
        return{
            'name': 'Match',
            'type': 'ir.actions.act_window',
            'res_model': 'cricket.matches',
            'view_mode': 'list,form',
            'domain': [('tournament_id', '=', self.id)],
        }

    def view_teams(self):
        '''view teams on smart button'''
        return {
            'name': 'Team',
            'type': 'ir.actions.act_window',
            'res_model': 'cricket.team',
            'view_mode': 'list,form',
            'domain': [('tournament_id', '=', self.id)],
        }