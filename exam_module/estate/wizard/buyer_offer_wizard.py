from odoo import models, fields, api, tools


class BuyerOfferWizard(models.TransientModel):
    _name = "buyer.offer.wizard"
    _description = "Buyer Offer Wizard"

    buyer_id = fields.Many2many("res.partner", string="Buyer", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    def action_buyer_offer_export(self):
        buyer_ids = ','.join(map(str, self.buyer_id.ids))

        return {
                'type': 'ir.actions.act_url',
                'url': f'/export/buyer_offer_report_xlsx?start_date={self.start_date}&end_date={self.end_date}&buyer_id={buyer_ids}',
                'target': 'self',
            }
