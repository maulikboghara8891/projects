from odoo import models, fields,api

class User(models.Model):
    _inherit = 'res.users'

    product_type = fields.Selection([
        ('ac', 'AC'),
        ('washing_machine ', 'Washing Machine '),
        ('fridge', 'Fridge')
    ])

    # service_type = fields.Selection([
    #     ('installation', 'Installation'),
    #     ('repair', 'Repair'),
    #     ('aMC_Service', 'AMC Service')
    # ])
