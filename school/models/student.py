from datetime import date
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Student(models.Model):
    _name = 'student.student'
    _description = 'Student'
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner', string='name')
    user_id = fields.Many2one('res.users')
    email = fields.Char(related="partner_id.email", string='email')
    phone_no = fields.Char(related="partner_id.phone", string='phone number')
    dob = fields.Date(string='Date of Birth')
    current_date = fields.Date(string='Current Date', default=date.today())
    age = fields.Integer(string='Age', compute='_compute_age')
    street = fields.Char(related="partner_id.street", string='Street')
    street2 = fields.Char(related="partner_id.street2", string='Street 2')
    zip = fields.Char(related="partner_id.zip", string='Zip', change_default=True)
    city = fields.Char(related="partner_id.city", string='City')
    state = fields.Selection([('draft', 'Draft'),
                              ('in_admission', 'In Admission'),
                              ('approved', 'Approved'),
                              ('running', 'Running'),
                              ('terminated', 'Terminated'),
                              ('alumni', 'Alumni')], default="draft", string='state')

    state_id = fields.Many2one("res.country.state", related="partner_id.state_id",
                               string='State',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', related="partner_id.country_id",
                                 string='Country', )
    image = fields.Binary(related='partner_id.image_1920')
    standard_id = fields.Many2one("standard.standard", string='Standard')
    subject_ids = fields.One2many('subject.subject', 'studant_id', string='subject')
    sub_m2m_ids = fields.Many2many('subject.subject')
    hobby_ids = fields.Many2many('hobby.hobby', string="Hobby")
    exam_result_ids = fields.One2many('exam.result', 'student_id', string="Exam")



    def object_to_action(self):
        return {
            "type": "ir.actions.act_window",
            'view_mode': 'list,form',
            "res_model": 'standard.standard',
        }
        self.state = 'in_admission'

    def stat_check(self):
        if self.state == 'approved':
            raise ValidationError(" if done state after not changes")

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            rec.age = 0
            if rec.dob:
                rec.age = date.today().year - rec.dob.year

    # @api.depends('marks')
    # def _compute_result(self):
    #     for rec in self:
    #         rec.pr=0
    #         rec.result=""
    #         if rec.marks>35:
    #             rec.pr=(rec.marks/100)*100
    #             rec.result="pass"
    #         else:
    #             rec.result="fail"
