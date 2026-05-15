from odoo import models, fields, api
from datetime import date, datetime


class CrmLead(models.Model):
    _inherit = 'crm.lead'


    parent_lead_id = fields.Many2one('crm.lead', string="Parent Lead")

    # country_id = fields.Many2one('res.country',string='Country')
    @api.onchange('expected_revenue', 'country_id')
    def sales_user_find(self):
        revenue = self.env['assignment.rule'].search([
            ('revenue_val', '<=', self.expected_revenue)
        ], order='revenue_val DESC', limit=1)
        country = self.env['assignment.rule'].search([
            ('country_id', '=', self.country_id)
        ], limit=1)

        total_score = 0
        if country:
            total_score += country.score
        if revenue:
            total_score += revenue.score

        user = self.env['auto.assignment'].search([
            ('min_score', '>=', total_score),
            ('country_id', '=', self.country_id)
        ], order='min_score asc', limit=1)

        self.user_id = user.user_id

    original_lead_id = fields.Many2one('crm.lead', string="Original Lead")

    def _cron_lead_activity_check(self):
        leads = self.env['crm.lead'].search([
            ('active', '=', True),
        ], limit=5)
        today = date.today()

        for lead in leads:
            last_activity = (lead.activity_date_deadline or lead.write_date.date())

            day = (today - last_activity).days
            if day >= 15 and day <= 30:
                print(lead)

                activity = self.env['mail.activity.type'].search([
                    ('name', '=', 'follow-up')
                ], limit=1)
                if not activity:
                    self.env['mail.activity.type'].create({
                        'name': 'follow-up',
                        'summary': 'do not new lead create'
                    })
                self.env['mail.activity'].create({
                    'res_id': lead.id,
                    'res_model_id': self.env['ir.model']._get_id('crm.lead'),
                    'activity_type_id': activity.id,
                    'summary': 'Follow-up',
                    'user_id': lead.user_id.id,
                })

            elif day > 30 and day < 45:
                print(lead)
                tag = self.env['crm.tag'].search([('name','=','re engagement')],limit=1).id
                existing = self.search([
                    ('parent_lead_id', '=', lead.id),
                    ( 'name','=', f'Re-engagement Required - {lead.name}')
                ], limit=1)

                if existing:
                    continue

                self.create({
                    'name': f'Re-engagement Required - {lead.name}',
                    'user_id': lead.user_id.id,
                    'parent_lead_id': lead.id,
                    'tag_ids':[(4,tag)] ,
                })

            elif day >= 45:
                print(lead)
                tag = self.env['crm.tag'].search([('name','=','high risk')],limit=1).id

                existing = self.search([
                    ('parent_lead_id', '=', lead.id),
                    ('name', '=', f'high risk - {lead.name}')
                ], limit=1)

                if existing:
                    continue

                self.create({
                    'name': f'high risk - {lead.name}',
                    'user_id': lead.user_id.id,
                    'parent_lead_id': lead.id,
                    'tag_ids':[(4, tag)] ,
                })



class SalesOrder(models.Model):
    _inherit = 'sale.order'

    def action_done(self):
        return self._create_invoices()
