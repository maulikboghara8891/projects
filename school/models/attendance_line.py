from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Attendanceline(models.Model):
    _name = 'attendance.line'
    _description = 'Attendance Line'

    attendance_id = fields.Many2one("attendance.attendance",string="Attendance id")

    student_id = fields.Many2one("student.student", string="Student id")
    standard_id = fields.Char(related="student_id.standard_id.st_class",string="standard id")
    present = fields.Boolean(string='Present')
    absent = fields.Boolean(string='Absent')

    @api.onchange('present')
    def _onchange_present(self):
        for rec in self:
            if rec.present:
                rec.absent = False

    @api.onchange( 'absent')
    def _onchange_absent(self):
        for rec in self:
            if rec.absent:
                rec.present = False
