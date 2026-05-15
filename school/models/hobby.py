from odoo import models, fields


class Hobby(models.Model):
    _name = 'hobby.hobby'
    _description = 'Hobby '
    _rec_name = 'name'

    name = fields.Char(string='Name')
    student_ids = fields.Many2many('student.student', string='Student')
