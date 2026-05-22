
from odoo import models, fields,api

class Timesheet(models.Model):
    _name = 'timesheet.timesheet'

    project_id = fields.Many2one('project.project',string='Project')
    task_id = fields.Many2one('project.task')
    time_spent = fields.Float(related="task_id.effective_hours" ,string='Time spent')

    # total_time = fields.Float(
    #     string='Total Time',
    #     compute='_compute_total_time',
    #     store=True
    # )
    #
    # @api.depends('time_spent')
    # def _compute_total_time(self):
    #     for rec in self:
    #         total = sum(
    #             self.search([
    #                 ('project_id', '=', rec.project_id.id)
    #             ]).mapped('time_spent')
    #         )
    #         rec.total_time = total
