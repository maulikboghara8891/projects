from odoo import models, fields,api


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    currency_id = fields.Many2one('res.currency',compute='_compute_currency_id',string='Currency')
    handling_charges = fields.Monetary(currency_field='currency_id',string="Handling Charges")
    charges_created = fields.Boolean(string="Charges Created")
    # income_account_id = fields.Many2one(related='company_id.income_account_id', readonly=False, check_company=True)
    # expense_account_id = fields.Many2one(related='company_id.expense_account_id', readonly=False, check_company=True)

    def _compute_currency_id(self):
            self.currency_id = self.env.company.currency_id

    def view_journal_enty(self):
        jrnl = f"{self.name} Handling Charges"

        journal = self.env['account.move'].search([
            ('ref', '=', jrnl)
        ],limit=1)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Journal Entry',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': journal.id,
            'target': 'current',
        }

    def handling_charges_entry(self):

        pickings = self.search([
            ('picking_type_id.code', '=', 'outgoing'),
            ('charges_created', '=', False),
            ('state', '=', 'done')
        ])

        for picking in pickings:
            total_qty = sum(picking.move_ids.mapped('product_uom_qty'))
            total_amount = total_qty * picking.handling_charges
            move_vals = {
                'ref': f"{picking.name} Handling Charges",
                'line_ids': [
                    (0, 0, {
                        'name': 'Handling Charges Debit',
                        'account_id': picking.company_id.expense_account_id.id,
                        'debit': total_amount,
                        'credit': 0.0,
                    }),
                    (0, 0, {
                        'name': 'Handling Charges Credit',
                        'account_id': picking.company_id.income_account_id.id,
                        'debit': 0.0,
                        'credit': total_amount,
                    }),
                ]
            }

            journal = self.env['account.move'].create(move_vals)
            journal.action_post()

            picking.charges_created = True