# Copyright (c) 2013, Atrina Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = ["Missed Withholding Receipt Number::180"]
	return columns, data

def get_data(filters):
	if filters.from_no and filters.to_no:
		lst = frappe.db.sql("select withholding_receipt_no from `tabPurchase Invoice` where docstatus != 2 having withholding_receipt_no > {0} and withholding_receipt_no < {1}".format(filters.from_no, filters.to_no), as_list=True)
		print("lst ===> ",lst)
		if len(lst)>0:
			single_list = flatList = [ int(item) for elem in lst for (item) in elem]
			# single_list = [int(i) for i in single_list]
			res = []
			for i in range(filters.from_no,filters.to_no+1):
				if i not in single_list:
					res.append(i)
			res1 = []
			for i in res:
				res1.append([i])
			return res1
		else:
			res = []
			for i in range(filters.from_no,filters.to_no+1):
				res.append(i)
			res1 = []
			for i in res:
				res1.append([i])
			return res1
