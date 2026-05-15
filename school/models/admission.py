from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class admission(models.Model):
    _name = 'school.admission'
    _description = 'Admission'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    email = fields.Char(string='email')
    phone = fields.Char(string='phone number')
    dob = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age')
    class_id = fields.Many2one("standard.standard", string='standard')
    state = fields.Selection(
        [('inquiry', 'Inquiry'),('draft', 'Draft'), ('rejected', 'Rejected'), ('approved', 'Approved')],
         string='state')
    street = fields.Char(string='street')
    street2 = fields.Char(string='street2')
    city = fields.Char(string='city')
    zip = fields.Char(string='zip')
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    fees=fields.Integer(string='fees')


    @api.depends('fees')
    def fees_pay(self):
        for rec in self:
            if rec.fees >=25000:
                rec.state='approved'
                raise ValidationError("admission done")
            else:
                raise ValidationError(" fess pay minimum 25000 after approval")

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            rec.age = 0
            if rec.dob:
                rec.age = date.today().year - rec.dob.year


    def create_rec(self):
        for rec in self:

            partner = self.env['res.partner'].create(
                {
                'name': rec.name,
                'email': rec.email,
                'phone': rec.phone,
                'street': rec.street,
                'street2': rec.street2,
                'city': rec.city,
                'zip': rec.zip,
                'state_id': rec.state_id.id,
                'country_id': rec.country_id.id,
                })
            self.env['student.student'].create(
                {
                    'partner_id': partner.id,
                    'dob': rec.dob,
                    'age': rec.age,
                    'state':rec.state,
                    'standard_id': rec.class_id.id,
                })
            rec.state='approved'


    def stat_reject(self):
        for rec in self:
            rec.state='rejected'


    @api.model
    def write(self,vals):
        rec=super().write(vals)

    # def rec_update(self):
    #     print(self,"self")
        partner_model = self.env['res.partner']  # Example: Contacts
        partner = partner_model.search([('name', '=',self.name)], limit=1)
        if partner:
            partner.write({
                'name': self.name,
                'email': self.email,
                'phone': self.phone,
                'street': self.street,
                'street2': self.street2,
                'city': self.city,
                'zip': self.zip,
                'state_id': self.state_id.id,
                'country_id': self.country_id.id,
            })
            self.env['student.student'].search([('partner_id', '=',self.name)], limit=1).write(
                {

                    'partner_id': partner.id,
                    'dob': self.dob,
                    'age': self.age,
                    'state': self.state,
                    'standard_id': self.class_id,
                })

        return rec
