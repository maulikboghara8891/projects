from odoo import models, fields, api



class Attendance(models.Model):
    _name = 'attendance.attendance'
    _description = 'Attendance'
    _rec_name = 'standard_id'

    date = fields.Date(string='Date')
    standard_id = fields.Many2one('standard.standard', string='standard')
    student_ids = fields.One2many('attendance.line','attendance_id' ,string='Student')


