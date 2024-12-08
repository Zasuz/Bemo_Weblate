import logging
import json
from werkzeug.utils import redirect
from datetime import datetime

from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)



class MainController (http.Controller):
    @http.route('/', type='http', auth='public', csrf=False, website=True)
    def get_home_page(self, **kw):
        return request.render('branding.home_page_template')

    @http.route('/feedback', type='http', auth='public',methods=['POST'], csrf=False)
    def create_feedback(self, **kw):
        description = kw.get('description')
        _logger.info("description: %s", description)
        record = request.env['website.user.feedback'].sudo().create({
            'description': description,
            'create_datetime': datetime.now()
        })
        return redirect('/contactus-thank-you')

