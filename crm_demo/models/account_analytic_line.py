from odoo import models, fields,api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'


    related_task_id = fields.Many2one("project.task", string="Related Task")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super().create(vals_list)
    #     for rec in res:
    #         if self.env.context.get('is_related_task_timesheet'):
    #             rec.related_task_id = rec.task_id