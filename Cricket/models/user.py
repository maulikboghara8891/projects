from odoo import models, fields,api
from datetime import date

class BaseUser(models.Model):
    _inherit = 'res.users'



    dob = fields.Date(string="DOB", requirbed=True)


