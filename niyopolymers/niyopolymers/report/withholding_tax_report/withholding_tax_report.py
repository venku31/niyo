# Copyright (c) 2013, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["ID:Link/Purchase Invoice:200", "TIN:Data:120", "Supplier Name::200", "Region::150", "K-Ketema::150", "Woreda::150", "House No.::150", "Withholding Type::150", "Taxable Amount:Currency:150", "Tax Withheld:Currency:150", "Withholding Tax Receipt Number:Data:150", "Withholding Tax Receipt Date:Date:150"]
	data = get_data(filters)
	return columns, data

def get_data(filters):
	if filters.from_no and filters.to_no:
		return frappe.db.sql("""
			SELECT
				pi.name,
				pi.tax_id,
				pi.supplier_name,
				a.state,
				a.county,
				a.city,
				a.address_line1,
				s.withholding_category,
				pi.net_total,
				ptc.tax_amount,
				pi.withholding_receipt_no,
				pi.withholding_receipt_date
			FROM
				`tabPurchase Invoice` as pi,
				`tabSupplier` as s,
				`tabPurchase Taxes and Charges` as ptc,
				`tabAddress` as a
			WHERE
				s.name = pi.supplier
				AND ptc.parent = pi.name
				AND ptc.account_head = '21130 - WTH Tax Payable - NP'
				AND pi.docstatus='1'
				AND a.name = pi.supplier_address
				AND pi.withholding_receipt_date between '{0}' and '{1}'
				AND pi.withholding_receipt_no between {2} and {3}
		""".format(filters.from_date, filters.to_date, filters.from_no, filters.to_no))
	else:
		return frappe.db.sql("""
			SELECT
				pi.name,
				pi.tax_id,
				pi.supplier_name,
				a.state,
				a.county,
				a.city,
				a.address_line1,
				s.withholding_category,
				pi.net_total,
				ptc.tax_amount,
				pi.withholding_receipt_no,
				pi.withholding_receipt_date
			FROM
				`tabPurchase Invoice` as pi,
				`tabSupplier` as s,
				`tabPurchase Taxes and Charges` as ptc,
				`tabAddress` as a
			WHERE
				s.name = pi.supplier
				AND ptc.parent = pi.name
				AND ptc.account_head = '21130 - WTH Tax Payable - NP'
				AND pi.docstatus='1'
				AND a.name = pi.supplier_address
				AND pi.withholding_receipt_date between '{0}' and '{1}'
		""".format(filters.from_date, filters.to_date))
