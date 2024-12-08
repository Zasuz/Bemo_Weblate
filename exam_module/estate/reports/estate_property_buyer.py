import logging

from odoo import models, fields, api, tools

_logger = logging.getLogger(__name__)


class EstatePropertyBuyer(models.Model):
    _name = 'estate.property.buyer'
    _auto = False

    buyer_id = fields.Many2one('res.partner', string='Buyer')
    count_property_accepted = fields.Integer()
    count_property_canceled = fields.Integer()
    count_property_sold = fields.Integer()
    count_offer_accepted = fields.Integer()
    count_offer_refused = fields.Integer()
    max_offer_price = fields.Float()
    min_offer_price = fields.Float()

    def _get_sql_statement(self, start_date=False, end_date=False, buyer_id=False):
        sql_primary = f"""
                row_number() OVER () as id,
                p.buyer_id,
                COUNT(DISTINCT CASE WHEN p.stage = 'offer_accepted' THEN p.id END) as count_property_accepted,
                COUNT(DISTINCT CASE WHEN p.stage = 'sold' THEN p.id END) as count_property_sold,
                COUNT(DISTINCT CASE WHEN p.stage = 'canceled' THEN p.id END) as count_property_canceled,
                COUNT(DISTINCT CASE WHEN o.status = 'accepted' THEN o.id END) as count_offer_accepted,
                COUNT(DISTINCT CASE WHEN o.status = 'refused' THEN o.id END) as count_offer_refused,
                MAX(o.price) as max_offer_price,
                MIN(o.price) as min_offer_price
            FROM estate_property p
            LEFT JOIN estate_property_offer o ON p.id = o.property_id
        """
        if start_date and end_date:
            sql_statement = f"AND p.availability_date >= '{start_date}' AND p.availability_date <= '{end_date}'"
            if buyer_id:
                sql_statement += f" AND p.buyer_id IN ({buyer_id})"
                _logger.info(sql_statement)
            return f"""
                SELECT
                    rp.name as buyer_name,
                    rp.email as buyer_email,
                    {sql_primary}
                LEFT JOIN res_partner rp ON p.buyer_id = rp.id
                WHERE p.buyer_id IS NOT NULL
                {sql_statement}
                GROUP BY p.buyer_id, rp.name, rp.email
            """
        else:
            return f"""
                CREATE OR REPLACE VIEW estate_property_buyer AS (
                    SELECT
                       {sql_primary}
                    WHERE p.buyer_id IS NOT NULL
                    GROUP BY p.buyer_id
                )
            """


    def query_buyer_offer_with_dates(self, start_date=None, end_date=None, buyer_id=None):
        sql_statement = self._get_sql_statement(start_date, end_date,buyer_id)
        self._cr.execute(sql_statement)
        result = self._cr.dictfetchall()
        return result

    def init(self):
        tools.drop_view_if_exists(self._cr, 'estate_property_buyer')
        sql_statement = self._get_sql_statement()
        self._cr.execute(sql_statement)
