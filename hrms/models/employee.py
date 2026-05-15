from odoo import models, fields,api
from datetime import date

class employee(models.Model):
    _name = 'employee.employee'
    _description = 'Employee'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='name')
    email = fields.Char(related="partner_id.email", string='email')
    phone_no = fields.Char(related="partner_id.phone", string='phone number')
    position = fields.Char( string='position ')
    join_date = fields.Date(string='Joining Date')
    experience = fields.Integer(string='Experience')
    salary = fields.Integer(string='Salary')
    street = fields.Char(related="partner_id.street", string='Street')
    street2 = fields.Char(related="partner_id.street2", string='Street 2')
    zip = fields.Char(related="partner_id.zip", string='Zip', change_default=True)
    city = fields.Char(related="partner_id.city", string='City')
    status = fields.Selection(   [('active', 'Active'), ('inactive', 'In Active')], default="active", string='status')
    # subject_id = fields.Many2one('subject.subject', string='subject')
    # standard_id = fields.Many2one("standard.standard", string='Standard')
    state_id = fields.Many2one("res.country.state", related="partner_id.state_id", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', related="partner_id.country_id", string='Country', ondelete='restrict')
    image = fields.Binary(related='partner_id.image_1920')

    description = fields.Char(string='Description')

    # main_file = fields.char('File')