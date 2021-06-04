# Copyright (c) 2013, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["TIN NO:Int:150"]+["Employee Name:Data:200"]+["Date of Employeement:Date:100"]+["Monthly Salary (Silver):Float:150"]+[" Employer contribution amount 7% (Birr):Float:100"]+[" Employer contribution amount 11% (Birr):Float:100"]+[" Collective contribution by employer 18% / Silver / (F + G):Float:200"]
	data = get_data(filters)
	return columns, data

def get_data(filters):
	if filters:
		return frappe.db.sql("""
			Select
				emp.tin_no,
				emp.employee_name,
				emp.date_of_joining,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)'),
				(select sd.amount from `tabSalary Detail` sd where  sd.parent=ss.name and emp.name=ss.employee and sd.salary_component='Pension (የጡረታ አበል) (7%)' ),
				(select sd.amount from `tabSalary Detail` sd where  sd.parent=ss.name and emp.name=ss.employee and sd.salary_component='Pension (የጡረታ አበል) (11%)' ),
				((select sd.amount from `tabSalary Detail` sd where  sd.parent=ss.name and emp.name=ss.employee and sd.salary_component='Pension (የጡረታ አበል) (7%)')+(select sd.amount from `tabSalary Detail` sd where  sd.parent=ss.name and emp.name=ss.employee and sd.salary_component='Pension (የጡረታ አበል) (11%)'))
			from
				`tabEmployee` as emp
			join
				`tabSalary Slip` as ss
			on
				emp.name = ss.employee
			where emp.date_of_joining between '{0}' and '{1}'
		""".format(filters['from_date'], filters['to_date']))
	else:
		return frappe.db.sql("""
			Select
				emp.tin_no,
				emp.employee_name,
				emp.date_of_joining,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)'),
				(select sd.amount from `tabSalary Detail` sd where  sd.parent=ss.name and emp.name=ss.employee and sd.salary_component='Pension (የጡረታ አበል) (7%)' ),
				(select sd.amount from `tabSalary Detail` sd where  sd.parent=ss.name and emp.name=ss.employee and sd.salary_component='Pension (የጡረታ አበል) (11%)' ),
				((select sd.amount from `tabSalary Detail` sd where  sd.parent=ss.name and emp.name=ss.employee and sd.salary_component='Pension (የጡረታ አበል) (7%)')+(select sd.amount from `tabSalary Detail` sd where  sd.parent=ss.name and emp.name=ss.employee and sd.salary_component='Pension (የጡረታ አበል) (11%)'))
			from
				`tabEmployee` as emp
			join
				`tabSalary Slip` as ss
			on
				emp.name = ss.employee

		""")	