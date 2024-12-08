from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
import logging
from odoo.exceptions import UserError
from odoo.tools import float_is_zero

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    availability_date = fields.Date(string='Available From', copy=False,
                                    default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True,
                                 copy=False)
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Number of Facades')
    has_garage = fields.Boolean(string="Has Garage ?")
    has_garden = fields.Boolean(string="Has Garden ?")
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    is_active = fields.Boolean(string='Active', default=True)
    stage = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='Stage', default='new', copy=False, required=True)
    best_price = fields.Float(string='Best Price', compute='_compute_best_price', store=True)
    total_area = fields.Integer(string='Total Area', compute="_compute_total_area", store=True)

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    seller_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    code = fields.Char(string="Code", readonly=True, copy=False)

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price >= 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The expected price must be strictly positive.')
    ]

    def unlink(self):
        for record in self:
            if record.stage not in ['new', 'canceled'] and not self.env.context.get("by_pass_check"):
                raise UserError("The state must be in 'New' or 'Canceled' to delete.")
            return super(EstateProperty, self).unlink()

    @api.constrains('expected_price',"selling_price")
    def _check_selling_price_value(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and record.selling_price < record.expected_price * 0.9:
                raise UserError("The selling price must be at least 90% of the expected price")

    @api.model
    def default_get(self, fields_list):
        res = super(EstateProperty, self).default_get(fields_list)

        if 'buyer_id' in res and res['buyer_id']:
            buyer = self.env['res.partner'].browse(res['buyer_id'])

            res['buyer_email'] = buyer.email if buyer.email else self.env['res.partner'].search([], limit=1).email
        return res

    @api.model
    def create(self, vals):
        vals["code"] = self._generate_code()
        self._check_availability_date(vals.get('availability_date'))
        _logger.info("success")
        return super().create(vals)

    def write(self, vals):
        self._check_availability_date(vals.get('availability_date'))
        _logger.info("success")
        return super().write(vals)

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            if record.living_area or record.garden_area:
                record.total_area = record.living_area + record.garden_area
            else:
                record.total_area = 0

    @api.onchange("has_garden")
    def _onchange_has_garden(self):
        if not self.has_garden:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange("availability_date")
    def _onchange_availability_date(self):
        if self.availability_date:
            if self.availability_date < fields.Date.today():
                return {"warning": {"title": _("Warning"), "message": _("Date is must not in the past")}}

    def _check_availability_date(self, date):
        if date and fields.Date.from_string(date) < fields.Date.today():
            raise UserError(_("Date must not be in the past"))

    def _generate_code(self):
        existing_code = self.env['estate.property'].search([]).mapped('code')
        existing_number = []

        # Lấy các thứ tự đã tồn tại trong DB
        for code in existing_code:
            if code:
                number = int(code[3:])
                existing_number.append(number)

        # Tìm ra vị tri của thứ tự còn thiếu
        number_nulled = 1;
        while number_nulled in existing_number:
            number_nulled += 1
        # Format EPTxxxxx
        return "EPT" + str(number_nulled).zfill(5)

    def estate_property_action_sold(self):
        for record in self:
            if record.stage == "canceled":
                raise UserError("Cannot set a canceled property to sold")
            if record.stage == "sold":
                raise UserError("Property already sold")
            record.write({'stage': 'sold'})
            return True

    def estate_property_action_cancel(self):
        for record in self:
            if record.stage == "sold":
                raise UserError("Cannot set a sold property to canceled")
            if record.stage == "canceled":
                raise UserError("Property already canceled")
            record.write({'stage': 'canceled'})