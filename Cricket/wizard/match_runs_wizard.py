from odoo import models, fields,_

class MatchRuns(models.TransientModel):
    _name = 'match.runs.wizard'
    _description = "Match Runs"

    team_a_run=fields.Integer(string="Team A Run")
    team_b_run=fields.Integer(string="Team b Run")
    team_a_wickets=fields.Integer(string="Team A Wickets")
    team_b_wickets=fields.Integer(string="Team B Wickets")

    def action_confirm(self):
        record = self.env['cricket.matches'].browse(self.env.context.get('active_id'))

        # Update existing record
        record.write({
            'team_a_runs': record.team_a_runs + self.team_a_run,
            'team_b_runs': record.team_b_runs+ self.team_b_run,
            'team_a_wickets':record.team_a_wickets+ self.team_a_wickets,
            'team_b_wickets': record.team_b_wickets+ self.team_b_wickets,
        })


