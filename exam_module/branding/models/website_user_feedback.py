from odoo import models, fields, api


class WebsiteUserFeedback(models.Model):
    _name = 'website.user.feedback'
    _description = 'Website User Feedback'

    description = fields.Text(string='Description', required=True)
    create_datetime = fields.Datetime(string='Create Date', default=fields.Datetime.now)