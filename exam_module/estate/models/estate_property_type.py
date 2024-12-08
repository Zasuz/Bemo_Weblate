from odoo import fields, models, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(string="Name", required=True)
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    expected_price = fields.Float(string='Expected Price',related="property_ids.expected_price")
    stage = fields.Selection(related="property_ids.stage")
    #SQL Constraint
    _sql_constraints = [
        ('check_property_type_name', 'UNIQUE(name)', 'Name must be unique.')
    ]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # Python Constraint
    # @api.constrains('name')
    # def _check_unique_name(self):
    #     for record in self:
    #         names = self.search([('id', '!=', record.id), ('name', '=ilike', record.name)])
    #         if names:
    #             raise UserError("Name must be unique")
