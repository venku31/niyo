# Copyright (c) 2013, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = ["Employer Tax Account::150"]+["Employer Enterprise No::150"]+["TIN NO::150"]+["Employee Name::200"]+["Start Date:Date:100"]+["End Date:Date:100"]+["Basic::100"]+[" Employee contribution amount 7% ::100"]+[" Employer contribution amount 11%::100"]+[" Total Contribution::100"]
	data = get_data(filters)
	return columns, data

def get_data(filters):
	if 'start_date' in filters:
		return frappe.db.sql("""
			Select
				c.employer_tax_Account,
				c.employer_enterprise_no,
				emp.tin_no,
				emp.employee_name,
				ss.start_date,
				ss.end_Date,
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
			join 
				`tabCompany` as c
			on
				ss.company = c.name
			where ss.start_date ='{0}'
		""".format(filters['start_date']))
	elif 'end_date' in filters:
		return frappe.db.sql("""
			Select
				c.employer_tax_Account,
				c.employer_enterprise_no,
				emp.tin_no,
				emp.employee_name,
				ss.start_date,
				ss.end_Date,
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
			join 
				`tabCompany` as c
			on
				ss.company = c.name
			where ss.end_date ='{0}'
		""".format(filters['end_date']))
	if 'start_date' in filters and 'end_date' in filters:
		return frappe.db.sql("""
			Select
				c.employer_tax_Account,
				c.employer_enterprise_no,
				emp.tin_no,
				emp.employee_name,
				ss.start_date,
				ss.end_Date,
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
			join 
				`tabCompany` as c
			on
				ss.company = c.name
			where ss.start_date = '{0}' and ss.end_date='{1}'
		""".format(filters['start_date'], filters['end_date']))
	else:
		return frappe.db.sql("""
			Select
				c.employer_tax_Account,
				c.employer_enterprise_no,
				emp.tin_no,
				emp.employee_name,
				ss.start_date,
				ss.end_Date,
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
			join 
				`tabCompany` as c
			on
				ss.company = c.name
		""")	