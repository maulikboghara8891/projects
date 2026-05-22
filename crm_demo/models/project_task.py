from odoo import models, fields, api


class ProjectTaksk(models.Model):
    _inherit = 'project.task'

    assignee_id = fields.Many2one('res.users', string='Assignee')
    display_task = fields.Boolean(string='Display Task')

    total_time_spent = fields.Float(
        string='Total Time',
        compute='_compute_total_time_spent'
    )

    @api.depends('project_id')
    def _compute_total_time_spent(self):
        for rec in self:
            task_ids = self.env['account.analytic.line'].search([
                ('project_id', '=', rec.project_id.id), ("related_task_id", "=", self.id)
            ])
            rec.total_time_spent = sum(task_ids.mapped('unit_amount'))

    def action_project_timesheet(self):
        '''record in same project_id and display_task that record create'''
        task_ids = self.env['account.analytic.line'].search([
            ('project_id', '=', self.project_id.id), ("related_task_id", "=", self.id)
        ])
        # print(task_ids)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Task',
            'res_model': 'account.analytic.line',
            'view_mode': 'list',
            'view_id': self.env.ref('crm_demo.project_project_view_list').id,
            'domain': [('id', 'in', task_ids.ids)],
            'context': {"is_related_task_timesheet": True, "default_related_task_id": self.id,
                        "default_project_id": self.project_id.id}
        }
