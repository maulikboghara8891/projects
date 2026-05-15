from odoo import models, fields, api
from datetime import date


class Teacher(models.Model):
    _name = 'teacher.teacher'
    _description = 'Teachers data'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='name')
    email = fields.Char(related="partner_id.email", string='email')
    phone_no = fields.Char(related="partner_id.phone", string='phone number')
    dob = fields.Date(string='Date of Birth')
    current_date = fields.Date(string='Current Date', default=date.today())
    age = fields.Integer(string='Age', compute='_compute_age')
    street = fields.Char(related="partner_id.street", string='Street')
    street2 = fields.Char(related="partner_id.street2", string='Street 2')
    zip = fields.Char(related="partner_id.zip", string='Zip', change_default=True)
    city = fields.Char(related="partner_id.city", string='City')
    state = fields.Selection(
        [('draft', 'Draft'), ('in_admission', 'In Admission'), ('running', 'Running'), ('terminated', 'Terminated'),
         ('alumni', 'Alumni')], default="draft", string='Target Window')
    subject_id = fields.Many2one('subject.subject', string='subject')
    standard_id = fields.Many2one("standard.standard", string='Standard')
    state_id = fields.Many2one("res.country.state", related="partner_id.state_id", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', related="partner_id.country_id", string='Country', ondelete='restrict')

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            rec.age = 0
            if rec.dob:
                rec.age = date.today().year - rec.dob.year
