# Copyright (c) 2013, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	data = get_data()
	columns = ["Withholder's Tax account::180"]+["Withholdee's TIN::150"]+["Withholdee Name::150"]+["Receipt No::150"]+["Receipt Date::150"]+["Taxable Amount::150"]+["Tax withheld::150"]	
	return columns, data

def get_data():
	res = frappe.db.sql("""
	select c.withholder_tax_account, p.tax_id, p.supplier, p.withholding_receipt_no, p.withholding_receipt_date, p.total, a.tax_amount from `tabPurchase Invoice` as p join `tabPurchase Taxes and Charges` as a on p.name = a.parent join `tabCompany` as c on p.company = c.name and a.description like '%With Holding%' and rate = 2
	""")

	return res
