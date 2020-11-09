# coding: utf-8
from datetime import datetime
from odoo import models, _


class PaymentGroupReport(models.AbstractModel):
    _name = "report.account_payment_group_xlsx_report.payment_report_xlsx"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, objs):

        #
        # Helper Method
        #
        def _format_date(date_utc_format):
            """Change the UTC format used by Odoo for dd-mm-yyyy

            Arguments:
                date_utc_format {str} -- Date UTC format yyyy-mm-dd

            Returns:
                str -- Date in dd-mm-yyyy format.
            """
            date_d_m_y_format = datetime.strptime(date_utc_format, '%Y-%m-%d').strftime('%d-%m-%Y')
            return date_d_m_y_format

        #
        # Formatting
        #
        heading_format = workbook.add_format({
            "align": "center",
            "valign": "vcenter",
            "bold": True,
            "size": 14,
            "bg_color": "#C8E6C9"
        })

        sub_heading_format = workbook.add_format({
            "align": "center",
            "valign": "vcenter",
            "bold": True,
            "size": 12,
            "bg_color": "#FFF9C4"
        })

        sub_heading_taxes_format = workbook.add_format({
            "align": "center",
            "valign": "vcenter",
            "bold": True,
            "size": 12,
            "bg_color": "#FFAB91"
        })

        center_format = workbook.add_format({
            "align": "center",
            "valign": "vcenter",
        })

        monetary_format = workbook.add_format({
            "num_format": "AR$ #,##0.00",
            "align": "center",
            "valign": "vcenter",
        })

        #
        # Adding Sheet
        #
        column = 0
        row = 0
        worksheet = workbook.add_worksheet(_("Payments"))

        #
        # Merging Columns and Rows
        #
        worksheet.merge_range("A1:C2", _("Supplier Payments Report"), heading_format)

        #
        # Payments Query
        #
        payment_objs = self.env['account.payment.group'].browse(data['payment_ids'])

        #
        # Column Titles
        #
        row += 3
        worksheet.write(row, column, _("Payment Date"), sub_heading_format)
        column += 1
        worksheet.write(row, column, _("Name"), sub_heading_format)
        column += 1
        worksheet.write(row, column, _("Partner"), sub_heading_format)
        column += 1
        worksheet.write(row, column, _("Payment Methods"), sub_heading_format)
        column += 1
        worksheet.write(row, column, _("Amount"), sub_heading_format)

        # Taxes Columns
        withholding_columns = {}
        curr_column = column

        for payment in payment_objs:
            for withholding in payment.payment_ids:
                if withholding.amount != 0 and withholding.journal_id.name == 'Retenciones':
                    if withholding.payment_method_description not in withholding_columns:
                        curr_column += 1
                        withholding_columns.update({
                            withholding.payment_method_description: curr_column
                        })

        for withholding_column in withholding_columns:
            column += 1
            worksheet.write(row, column, withholding_column, sub_heading_taxes_format)

        columns_added = len(withholding_columns)

        column += 1
        worksheet.write(row, column, _("Amount Without Withholding"), sub_heading_format)
        column += 1
        worksheet.write(row, column, _("Payment Currency"), sub_heading_format)
        column += 1
        worksheet.write(row, column, _("Payment Currency Rate"), sub_heading_format)
        column += 1

        #
        # Width of the Columns
        #
        for column in range(column):
            worksheet.set_column(row, column, 30)

        #
        # Invoices Manipulation
        #
        for payment in payment_objs:
            #
            # Writing row of every payment
            #
            column = 0
            row += 1
            worksheet.write(row, column, _format_date(payment.payment_date), center_format)
            column += 1
            worksheet.write(row, column, payment.display_name, center_format)
            column += 1
            worksheet.write(row, column, payment.partner_id.name, center_format)
            column += 1
            worksheet.write(row, column, payment.payment_methods, center_format)
            column += 1
            worksheet.write(row, column, payment.payments_amount, monetary_format)

            for wh in payment.payment_ids:
                for header, column_header in withholding_columns.items():
                    if wh.payment_method_description == header:
                        if wh.amount_company_currency == 0:
                            continue
                        worksheet.write(row, column_header, wh.amount_company_currency, monetary_format)

            column += (columns_added + 1)
            worksheet.write(row, column, payment.amount_total_without_withholdings, monetary_format)
            column += 1
            if payment.payment_currency_id.name != 0:
                worksheet.write(row, column, payment.payment_currency_id.name, center_format)
            column += 1
            if payment.payment_currency_rate != 0.0:
                worksheet.write(row, column, payment.payment_currency_rate, monetary_format)
