import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import email_re

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    buyer_email = fields.Char(string='Buyer Email')
    user_sold = fields.Many2one('res.users', string='User Sold')

    @api.onchange('buyer_id')
    def _on_change_buyer_id(self):
        if self.buyer_id.email:
            self.buyer_email = self.buyer_id.email
        else:
            self.buyer_email = False

    @api.model
    def create(self, vals):
        if vals.get('buyer_email'):
            self._check_validate_buyer_email(vals.get('buyer_email'))
        return super(EstateProperty, self).create(vals)

    def write(self, vals):
        if vals.get('buyer_email'):
            self._check_validate_buyer_email(vals.get('buyer_email'))
        return super(EstateProperty, self).write(vals)

    def _check_validate_buyer_email(self,buyer_email):
        _logger.info("buyer_email: %s", buyer_email)
        if not bool(email_re.match(buyer_email)):
            raise UserError(_("Email is not valid , please enter a valid email"))
        else:
            return True

    def estate_property_action_sold(self):
        if self.buyer_id:
            self.user_sold = self.env.user
            return super(EstateProperty, self).estate_property_action_sold()
        else:
            raise UserError(_("Please enter the buyer before marking the property as sold"))

    def action_send_email(self):
        template = self.env.ref('estate_send_email.estate_property_confirm_sold_email_template')
        if template:
            template.send_mail(self.id, force_send=True)

