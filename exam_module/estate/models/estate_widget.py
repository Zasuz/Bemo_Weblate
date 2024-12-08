import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class EstateWidget(models.Model):
    _name='estate.widget'

    name = fields.Char()
    color = fields.Integer()
    date = fields.Date()

    @api.model
    def count_records(self):
        count_records = len(self.search([('color', '!=', 0)]))
        _logger.info('count_records' + str(count_records))
        return count_records

