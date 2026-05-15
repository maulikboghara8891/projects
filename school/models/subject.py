from odoo import models, fields


class Subject(models.Model):
    _name = 'subject.subject'
    _description = 'Subject data'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    mark = fields.Float(string='Marks')
    sub_state = fields.Selection([('active', 'Active'), ('removed', 'Removed')], string='State', default='active')
    studant_id = fields.Many2one('student.student', string='Student id')
    standard_id = fields.Many2one("standard.standard", string='Standard')
