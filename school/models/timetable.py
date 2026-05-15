from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'standard.timetable'
    _description = 'timetable'



