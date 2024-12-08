import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    user_accepted = fields.Many2one('res.users')
    user_refused = fields.Many2one('res.users')

    def estate_property_offer_accept_action(self):
        res = super(EstatePropertyOffer, self).estate_property_offer_accept_action()
        for record in self:
            #By pass check status accpeted khong cho phep update
            self.with_context(bypass_status_check=True).write({'user_accepted': record.env.user.id})
            template = self.env.ref('estate_send_email.estate_property_offer_accepted_email_template')
            if template:
                template.send_mail(self.id, force_send=True)
            record.property_id._on_change_buyer_id()
        return res

    def estate_property_offer_refuse_action(self):
        for record in self:
            record.user_refused = record.env.user
        return super(EstatePropertyOffer, self).estate_property_offer_refuse_action()
