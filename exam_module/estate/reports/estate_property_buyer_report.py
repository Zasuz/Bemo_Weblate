import io
import xlsxwriter
import logging

from odoo import models, fields, api, tools

_logger = logging.getLogger(__name__)


class BuyerOfferReport(models.AbstractModel):
    _name = 'estate.report_estate_property_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, start_date, end_date, buyer_id):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Buyer Offers')

        headers = [
            'Buyer Name', 'Buyer Email', 'Property Accepted',
            'Property Canceled', 'Property Sold',
            'Offer Accepted', 'Offer Refused',
            'Max Offer Price', 'Min Offer Price'
        ]
        row_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#F2F2F2'})
        header_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#4F81BD', 'color': 'white',
             'border': 1})
        date_format = workbook.add_format(
            {'num_format': 'dd-mm-yyyy', 'align': 'center', 'valign': 'vcenter', 'border': 1})
        title_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 20, 'bg_color': '#4F81BD',
             'color': 'white', 'border': 1})

        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 30)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 10)
        sheet.set_column('I:I', 10)

        sheet.merge_range('A1:I3', "Estate Property Buyer Report", title_format)
        sheet.merge_range('C5:C6', 'Date From', header_format)
        sheet.merge_range('D5:D6', start_date, date_format)
        sheet.merge_range('F5:F6', 'Date To', header_format)
        sheet.merge_range('G5:G6', end_date, date_format)

        row = 10
        for col_num, header in enumerate(headers):
            sheet.write(row - 1, col_num, header, header_format)

        records = self.env['estate.property.buyer'].query_buyer_offer_with_dates(start_date=start_date,
                                                                                 end_date=end_date, buyer_id=buyer_id)

        for record in records:
            sheet.write(row, 0, record['buyer_name'] or '', row_format)
            sheet.write(row, 1, record['buyer_email'] or '', row_format)
            sheet.write(row, 2, record['count_property_accepted'] or 0, row_format)
            sheet.write(row, 3, record['count_property_canceled'] or 0, row_format)
            sheet.write(row, 4, record['count_property_sold'] or 0, row_format)
            sheet.write(row, 5, record['count_offer_accepted'] or 0, row_format)
            sheet.write(row, 6, record['count_offer_refused'] or 0, row_format)
            sheet.write(row, 7, record['max_offer_price'] or 0, row_format)
            sheet.write(row, 8, record['min_offer_price'] or 0, row_format)
            row += 1

        workbook.close()
        output.seek(0)

        return output.getvalue()
