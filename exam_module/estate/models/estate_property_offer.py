from datetime import timedelta
import logging

from odoo import fields, models, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    validity = fields.Integer(string='Validity (in days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline')

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', store=True,
                                       related='property_id.property_type_id')
    property_stage = fields.Selection(related="property_id.stage")
    _sql_constraints = [
        ("check_price_positive", "CHECK(price >= 0)", "Price must be positive")
    ]

    @api.model
    def create(self, vals):
        existing_price = self.env["estate.property.offer"].search(
            [("property_id", "=", vals.get("property_id")), ("price", ">", vals.get("price"))])
        if existing_price:
            raise UserError("Price must be higher than the existing offer")

        record = super(EstatePropertyOffer, self).create(vals)
        record.property_id.stage = "offer_received"
        _logger.info("Created offer with id: %s", record.id)
        return record

    def write(self, vals):
        for record in self:
            # Check xem trạng thái cũ của offer có phải là accepted không và trạng thái mới có được cập nhật thành refused không
            # Nếu thành refuse thì người dùng có thể cập nhật lại thông tin của offer
            if record.status and record.status == 'accepted' and vals.get('status') != 'refused' and not self.env.context.get('bypass_status_check') :
                raise UserError("Can not Edit/Delete Offer Accepted")
        res = super(EstatePropertyOffer, self).write(vals)
        return res

    def unlink(self):
        for record in self:
            if record.status and record.status == 'accepted':
                raise UserError("Can not Edit/Delete Offer Accepted")
        return super(EstatePropertyOffer, self).unlink()

    @api.depends('validity', "create_date")
    def _compute_deadline(self):
        for record in self:
            # _logger.info("create_date: %s", record.create_date)
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = None

    def estate_property_offer_accept_action(self):
        for record in self:
            record.status = "accepted"
            record.property_id.write({
                "buyer_id": record.partner_id.id,
                "selling_price": record.price
            })




    def estate_property_offer_refuse_action(self):
        for record in self:
            record.status = "refused"
