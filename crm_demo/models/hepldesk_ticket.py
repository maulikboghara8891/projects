from odoo import models, fields,api

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'


    service_type = fields.Selection([
        ('installation','Installation'),
        ('repair','Repair'),
        ('aMC_Service','AMC Service')
    ],tracking=True)
    product_type = fields.Selection([
        ('ac','AC'),
        ('washing_machine ','Washing Machine '),
        ('fridge','Fridge')
    ])
    brand = fields.Char(string="Brand")
    serial_number = fields.Char(string="Serial Number")
    warranty_status = fields.Selection([
        ('running','Running'),
        ('completed','Completed')
    ])

    # assign_person_id = fields.Many2one('res.users', string="Assign Person")

    @api.onchange('product_type')
    def sales_user_find(self):
        employee = self.env['res.users'].search([
            ('product_type','=',self.product_type)
        ],limit=1)
        if employee:
            self.user_id=employee.id
        else:
            self.user_id = False
