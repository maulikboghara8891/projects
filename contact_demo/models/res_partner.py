from odoo import models, fields,api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    confirm = fields.Boolean(string="Confirme")
    minimum = fields.Float(string="Minimum amount")


    @api.onchange('parent_id')
    def _parent_value_child_pass(self):
        for rec in self:
            parent = rec
            while parent.parent_id:
                parent = parent.parent_id
            rec.minimum = parent.minimum

    @api.constrains('confirm', 'parent_id')
    def _check_confirm_unique_per_parent(self):
        for rec in self:
            if not rec.confirm:
                continue
            parent = rec
            while parent.parent_id:
                parent = parent.parent_id

            # if rec !=parent  and  parent.confirm:
            #     raise ValidationError(
            #         "Only one contact can be confirmed in the same parent."
            #     )
            existing = self.search([
                ('id', 'child_of', parent.id),
                ('confirm', '=', True),
                ('type', '=', 'delivery'),
                ('id', '!=', rec.id),
                # '|',
                # ('id', '=', parent.id),

                                ], limit=1)

            if existing :
                raise ValidationError(
                    "Only one contact can be confirmed in the same parent."
                )

            # if rec.parent_id.confirm:
            #     raise ValidationError(
            #         "You cannot confirm this contact because a parent is already confirmed."
            #     )
                # parent = parent.parent_id
                #
                # children = self.search([
                #     ('id', 'child_of', rec.id),
                #     ('id', '!=', rec.id),
                #     ('confirm', '=', True)
                # ], limit=1)
                #
                # if children:
                #     raise ValidationError(
                #         "You cannot confirm this contact because a child contact is already confirmed."
                #     )
    # @api.constrains('confirm', 'parent_id')
    # def _check_confirm_unique_per_parent(self):
    #     for rec in self:
    #         if rec.confirm and rec.parent_id:
    #             print(rec.parent_id)
    #             existing = self.search([
    #                 ('parent_id', '=', rec.parent_id.id),
    #                 ('confirm', '=', True),
    #                 ('id', '!=', rec.id)
    #             ], limit=1)
    #
    #             if existing:
    #                 raise ValidationError(
    #                     "Only one confirmed contact is allowed per parent."
    #                 )