from odoo import models, fields,api


class MatchPlayerLine(models.Model):
    _name = 'match.player.line'
    _description = 'Match Player Line'

    match_id = fields.Many2one('cricket.matches', string='Match')
    team_id = fields.Many2one('cricket.team', string='Team')
    player_id = fields.Many2one('res.partner', string='Player')
    runs=fields.Integer(string='Runs')


