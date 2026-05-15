from odoo import models, fields


class Standard(models.Model):
    _name = 'standard.standard'
    _description = 'Standard '
    _rec_name = 'st_class'

    st_class = fields.Char(string='standard', )

    student_ids = fields.One2many('student.student', 'standard_id', string='Students')
    teacher_ids = fields.One2many('teacher.teacher','standard_id', string='Teacher')

    _class_uniq = models.Constraint(
        'unique (st_class)',
        'already exist!',
    )
