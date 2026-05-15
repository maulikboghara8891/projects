from odoo import models, fields,api
from datetime import date

class employee(models.Model):
    _name = 'department.department'
    _description = 'Department'


    name = fields.Char(string='Department')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

