from odoo import fields, models, api


class ResUser(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller_id', string='Properties',
                                   domain=[('availability_date', '>', fields.Date.today())])
