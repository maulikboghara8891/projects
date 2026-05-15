from odoo import models, fields,api

class ProjectTaksk(models.Model):
    _inherit = 'project.task'

    assignee_id = fields.Many2one('res.users',string='Assignee')