from odoo import models, fields, api


class Examresult(models.Model):
    _name = 'exam.result'
    _description = 'Exam Result'

    student_id = fields.Many2one('student.student', string='Student')
    exam_id = fields.Many2one('exam.exam', string='Exam')

    subject = fields.Char(related="exam_id.subject_id.name", string='Subject')
    total_mark = fields.Integer(related="exam_id.total_mark", string='Total Mark')
    passing_mark = fields.Integer(related="exam_id.passing_mark", string='passing  Mark')
    obtain_mark = fields.Integer(string='Obtain Mark')
    result = fields.Char(string='Result', compute='_compute_result')
    pr = fields.Float(string='Pr')

    @api.depends('obtain_mark')
    def _compute_result(self):
        for rec in self:
            rec.pr = 0
            rec.result = ""
            if rec.obtain_mark > rec.passing_mark:
                rec.pr = (rec.obtain_mark / 100) * 100
                rec.result = "pass"
            else:
                rec.result = "fail"
                rec.pr = (rec.obtain_mark / 100) * 100
