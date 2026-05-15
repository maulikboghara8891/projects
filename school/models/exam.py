from odoo import models, fields


class Exam(models.Model):
    _name = 'exam.exam'
    _description = 'Exam'
    _rec_name = 'exam'

    exam = fields.Char(string='Exam type')
    standard_id = fields.Many2one("standard.standard", string='Standard')
    subject_id = fields.Many2one('subject.subject', domain="[('standard_id','=',standard_id)]", string='subject')
    partner_ids = fields.Many2many('student.student', domain="[('standard_id','=',standard_id)]", string='Students')
    total_mark = fields.Integer(string='Total mark')
    passing_mark = fields.Integer(string='Passing mark')
