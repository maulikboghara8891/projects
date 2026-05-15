from odoo import models


class HelpdeskCreateFsmTask(models.TransientModel):
    _inherit = 'helpdesk.create.fsm.task'

    def _generate_task_values(self):
        res = super()._generate_task_values()
        res['user_ids'] = self.helpdesk_ticket_id.user_id
        if self.helpdesk_ticket_id.warranty_status == 'running':
            res['under_warranty'] = True
        return res