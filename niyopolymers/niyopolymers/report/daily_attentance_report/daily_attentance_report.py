# Copyright (c) 2013, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ['Employee:Link/Employee:250']+['Employee Name:Data:200']+['Shift:Link/Shift Type:250']+['Last In:Datetime:150']
	data = get_data(filters)
	return columns, data

def get_data(filters):
	if 'employee' in filters and 'shift' in filters:
		query = "where time >= '{0}' and time <= '{1}' and employee = '{2}' and shift = '{3}' ".format(filters['from_date'], filters['to_date'] ,filters['employee'], filters['shift'])
		return get_query(query)
	elif 'employee' in filters and 'shift' not in filters:
		query = "where time >= '{0}' and time <= '{1}' and employee = '{2}' ".format(filters['from_date'], filters['to_date'] ,filters['employee'])
		return get_query(query)	
	elif 'employee' not in filters and 'shift' in filters:
		query = "where time >= '{0}' and time <= '{1}' and shift = '{2}' ".format(filters['from_date'], filters['to_date'] ,filters['shift'])
		return get_query(query)	
	else: 
		query = "where time >= '{0}' and time <= '{1}' ".format(filters['from_date'], filters['to_date'])
		return get_query(query)

def get_query(query):
	return frappe.db.sql("""
		select employee, employee_name, shift, min(time) from `tabEmployee Checkin`
		{}
		group by employee,DATE(time) order by time desc
		""".format(query))	