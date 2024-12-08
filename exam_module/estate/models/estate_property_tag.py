from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color Index")
    _sql_constraints = [
        ('check_property_tag_name', 'unique(name)', 'Name must be unique')
    ]

    # @api.constrains('name')
    # def _check_unique_name(self):
    #     for record in self:
    #         if self.search([('id', '!=', record.id), ('name', '=ilike', record.name)]):
    #             raise UserError("Name must be unique.")
