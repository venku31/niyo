# Copyright (c) 2013, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json

def execute(filters=None):
	columns, data = [], []
	columns = ['Employee:Link/Employee:300']+['Employee Name:Data:250']+['Reporting Manager:Data:250']+['Date:Date:200']
	data = get_data(filters)
	return columns, data

def get_data(filters):
	query = frappe.db.sql("""
		select ver.creation, ver.docname, ver.data 
		from `tabVersion` as ver 
		where docname = '{}'
		order by ver.docname
	""".format(filters['employee']), as_dict=1)
	lst = []
	for i in query:
		dict_convert = json.loads(i['data'])
		if 'changed' in dict_convert:
			for j in dict_convert['changed']:
				if 'reporting_manager' in j:
					emp_name = frappe.db.get_value('Employee', i['docname'], 'employee_name')
					b = (i['docname'], emp_name, j[2], i['creation'])
					lst.append(b)
	return tuple(lst)			

