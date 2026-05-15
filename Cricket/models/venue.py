from odoo import models, fields

class CricketVenue(models.Model):
    _name = 'cricket.venue'
    _description = 'Cricket Venue'

    name = fields.Char('Stadium Name')
    street=fields.Char('Street Name')
    city = fields.Char('City')
    state = fields.Char('State')
    country = fields.Char('Country')
