from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    timesheet_line_ids = fields.One2many('timesheet.line', 'sale_order_id', string='Timesheet Lines', )
    timesheet_html = fields.Html(compute='_compute_timesheet_html')

    def action_timesheet_update(self):
        if not self.start_date or not self.end_date:
            raise UserError('Please specify start and end date')

        for rec in self:
            rec.timesheet_line_ids.unlink()
            tasks = rec.order_line.mapped('task_id')
            all_tasks = (
                    tasks |
                    tasks.mapped('parent_id') |
                    tasks.mapped('child_ids')
            )
            for task in all_tasks:
                last_date = rec.start_date - timedelta(days=30)
                last_month_lines = self.env['account.analytic.line'].search([
                    ('task_id', '=', task.id),
                    ('date', '>=', last_date),
                    ('date', '<=', rec.start_date)
                ])

                last_month_hours = sum(last_month_lines.mapped('unit_amount'))
                allocated_hours = task.allocated_hours
                allocated_hours += task.subtask_allocated_hours
                period_lines = self.env['account.analytic.line'].search([
                    ('task_id', '=', task.id),
                    ('date', '>=', rec.start_date),
                    ('date', '<=', rec.end_date)
                ])

                used_hours_period = sum(period_lines.mapped('unit_amount'))
                # used_hours_period=task.effective_hours+last_month_hours
                if used_hours_period:
                    self.env['timesheet.line'].create({
                        'sale_order_id': rec.id,
                        'task_id': task.id,
                        'parent_task_id': task.parent_id.id if task.parent_id else False,
                        'allocation_source': f'Inherited from {task.parent_id.name}' if task.parent_id else 'Task itself',
                        'source_allocated_hours': allocated_hours,
                        'allocated_hours': allocated_hours,
                        'total_used_hours': task.effective_hours,
                        'total_used_last_month': last_month_hours,
                        'used_hours_period': used_hours_period,
                        'remaining_hours': allocated_hours - task.effective_hours,
                    })
        return


    @api.depends('timesheet_line_ids')
    def _compute_timesheet_html(self):
        for rec in self:
            total_allocated = 0
            source_total_allocated = 0
            total_used = 0
            total_last = 0
            total_period = 0
            total_remaining = 0
            data = f"""
                    <h2>Timesheet Usage By Task</h2>
                    <p>
                        <b>Start Date:</b> {rec.start_date or ''}
                        &nbsp;&nbsp;
                        <b>End Date:</b> {rec.end_date or ''}
                    </p>
                    <table  width="100%" >
                        <tr>
                            <th><b>Task</b></th>
                            <th><b>Parent Task</b></th>
                            <th><b>Allocation Source</b></th>
                            <th><b>Source Allocated Hours</b></th>
                            <th><b>Allocated Hours</b></th>
                            <th><b>Total Used</b></th>
                            <th><b>Last Month</b></th>
                            <th><b>Used Period</b></th>
                            <th><b>Remaining</b></th>
                        </tr>
                """

            for line in rec.timesheet_line_ids:
                total_allocated += line.allocated_hours
                source_total_allocated += line.source_allocated_hours
                total_used += line.total_used_hours
                total_last += line.total_used_last_month
                total_period += line.used_hours_period
                total_remaining += line.remaining_hours

                data += f"""
                        <tr>
                            <td>{line.task_id.name or ''}</td>
                            <td>{line.parent_task_id.name or '-'}</td>
                            <td>{line.allocation_source or ''}</td>
                            <td>{line.source_allocated_hours:.2f}</td>
                            <td>{line.allocated_hours:.2f}</td>
                            <td>{line.total_used_hours:.2f}</td>
                            <td>{line.total_used_last_month:.2f}</td>
                            <td>{line.used_hours_period:.2f}</td>
                            <td>{line.remaining_hours:.2f}</td>
                        </tr>
                    """

            data += f"""
                    <tr>
                        <td colspan="3">
                            <b>Total</b>
                        </td>
                        <td><b>{source_total_allocated:.2f}</b></td>
                        <td><b>{total_allocated:.2f}</b></td>
                        <td><b>{total_used:.2f}</b></td>
                        <td><b>{total_last:.2f}</b></td>
                        <td><b>{total_period:.2f}</b></td>
                        <td><b>{total_remaining:.2f}</b></td>
                    </tr>
                </table>
                """
            rec.timesheet_html = data


class TimeSheetLine(models.Model):
    _name = 'timesheet.line'

    sale_order_id = fields.Many2one('sale.order')
    task_id = fields.Many2one('project.task', string='Task')
    parent_task_id = fields.Many2one('project.task', string='Parent Task')
    allocation_source = fields.Char()
    source_allocated_hours = fields.Float()
    allocated_hours = fields.Float()
    total_used_hours = fields.Float()
    total_used_last_month = fields.Float()
    used_hours_period = fields.Float()
    remaining_hours = fields.Float()
