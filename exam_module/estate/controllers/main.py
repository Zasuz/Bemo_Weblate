import logging
import json

from odoo import http
from odoo.http import request
from datetime import date

_logger = logging.getLogger(__name__)


class BuyerOfferController(http.Controller):
    @http.route('/export/buyer_offer_report_xlsx', type='http', auth='public')
    def export_buyer_offer_report_xlsx(self, **kw):
        start_date = kw.get('start_date')
        end_date = kw.get('end_date')
        buyer_id = kw.get('buyer_id')

        report_model = request.env['estate.report_estate_property_xlsx']
        file_content = report_model.generate_xlsx_report(start_date, end_date, buyer_id)
        headers = [
            ('Content-Disposition', 'attachment; filename="Buyer_Offers_Report.xlsx"'),
            ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        ]

        return request.make_response(file_content, headers=headers)

    @http.route("/shop/estate", type="http", auth="public", website=True)
    def get_shop_estate(self, page=1, limit=12, search='', **kw):
        page = int(page)
        limit = int(limit)
        offset = (page - 1) * limit
        total_products = request.env['estate.property'].search_count([('name', 'ilike', search)])

        total_pages = (total_products // limit) + (1 if total_products % limit > 0 else 0)
        if page < 0:
            page = 1
        if page > total_pages:
            page = total_pages

        estates = request.env['estate.property'].search([('name', 'ilike', search)], limit=limit, offset=offset)
        range_display = 2
        page_range = self.get_range_page(page, total_pages, range_display)

        return http.request.render('estate.estate_property_template', {
            'estates': estates,
            'page': page,
            'total_pages': total_pages,
            'limit': limit,
            'page_range': page_range,
            'search': search
        })

    @http.route('/shop/estate/<int:estate_id>', auth='public', website=True)
    def estate_detail(self, estate_id, **kw):
        # Lấy thông tin của tài sản theo ID
        estate = http.request.env['estate.property'].browse(estate_id)
        if not estate :
            return {
                "status": "error",
                "message": f"Could not find estate with ID: {id}"
            }

        if not estate.exists():
            return http.request.render('website.404')

        return http.request.render('estate.estate_property_detail_template', {
            'estate': estate
        })

    @http.route('/api/estate', type="http", auth="public", methods=['GET'], csrf=False, cors="*")
    def get_estate(self):
        estates = request.env['estate.property'].sudo().search([])

        return http.Response(
            json.dumps(estates.read(), cls=DateEncoder),
            content_type='application/json'
        )

    @http.route('/api/estate/<int:id>', auth="public", methods=['GET'], csrf=False, cors="*")
    def get_estate_by_id(self, id):
        estate = request.env['estate.property'].sudo().browse(id)
        if not estate.exists() :
            return http.Response(
                    status=404,
                    reponse="Could not find estate with ID: {id}",
                    content_type='application/json')

        return http.Response(
            json.dumps(estate.read(), cls=DateEncoder),
            content_type='application/json'
        )

    @http.route('/api/estate', type="json", auth="public", methods=['POST'], csrf=False, cors="*")
    def post_estate(self):
        data = request.jsonrequest
        request.env['estate.property'].sudo().create(data)
        return {
            "status": "success"
        }

    @http.route('/api/estate/<int:id>', type="json", auth="public", methods=['PUT'], csrf=False, cors="*")
    def put_estate(self, id):
        data = request.jsonrequest


        estate_fields = set(request.env['estate.property']._fields.keys())

        base_fields = set(['id', 'create_date', 'write_date', 'create_uid', 'write_uid'])
        _logger.info("base_fields: %s", ",".join(base_fields))

        thread_fields = set(request.env['mail.thread']._fields.keys())
        _logger.info("base_fields: %s", ",".join(thread_fields))

        activity_fields = set(request.env['mail.activity.mixin']._fields.keys())
        _logger.info("base_fields: %s", ",".join(activity_fields))

        # Tru các field ở model khác
        excluded_fields = base_fields | thread_fields | activity_fields
        specific_fields = estate_fields - excluded_fields
        _logger.info("specific_fields: %s", ",".join(specific_fields))

        missing_fields = [field for field in specific_fields if field not in data]
        if missing_fields:
            return {
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }

        estate = request.env['estate.property'].sudo().browse(id)
        if not estate.exists() :
            return {
                "status": "error",
                "message": f"Could not find estate with ID: {id}"
            }
        data['code'] = estate.code
        estate.sudo().write(data)
        return {
            "status": "success",
            "message": f"Updated estate with ID: {id}"
        }

    @http.route('/api/estate/<int:id>', type="json", auth="public", methods=['PATCH'], csrf=False, cors="*")
    def patch_estate(self, id):
        data = request.jsonrequest
        estate = request.env['estate.property'].browse(id)
        if not estate.exists() :
            return {
                "status": "error",
                "message": f"Could not find estate with ID: {id}"
            }
        estate.sudo().write(data)
        return {
                "status": "success",
                "message": f"Updated estate with ID: {id}"
        }

    @http.route('/api/estate/<int:id>', methods=['DELETE'], type="http", auth="public", csrf=False, cors="*")
    def delete_estate(self, id):
        estate = request.env['estate.property'].browse(id)
        if not estate.exists():
            return http.Response(
                status=404,
                content_type="application/json",
                response=json.dumps({
                    "status": "error",
                    "message": f"Could not find estate with ID: {id}"
                })
            )
        estate.with_context(by_pass_check=True).sudo().unlink()
        return http.Response(
            status=200,
            content_type="application/json",
            response=json.dumps({
                "status": "success",
                "message": f"Deleted estate with ID: {id}"
            })
        )

    def get_range_page(self, current_page, total_pages, range_display=2):
        start_range = max(1, current_page - range_display)
        end_range = min(total_pages, current_page + range_display)
        return range(start_range, end_range + 1)


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)
