from odoo import models, fields

class dr(models.Model):
    _name = 'dr.dr'
    _description = 'Hospital'
    _rec_name = 'name'


    name = fields.Char(string='Name')