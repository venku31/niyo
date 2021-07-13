# Copyright (c) 2013, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = ["Employer Tax Account::180"]+["Employer Enterprise No::150"]+["Employee's TIN::150"]+["Employee Name::150"]+["Start Date:Date:150"]+["End Date:Date:150"]+["Basic::150"]+["Total Transportation Allowance::150"]+["Taxable Transportation Allowance::150"]+["Overtime::150"]+["Other Taxable benefits::150"]+["Taxable Amount::150"]+["Tax Withheld::150"]+["Cost Sharing::150"]	
	return columns, data

def get_data(filters):
	if 'start_date' in filters:
		res = frappe.db.sql("""
				Select
				c.employer_tax_account,
				c.employer_enterprise_no,
				emp.tin_no,
				emp.employee_name,
				ss.start_date,
				ss.end_Date,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)') as basic,
				"" as total_transportation_allowance,
				"" as total_transportation_allowance,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Overtime (ተጨማሪ ሰአት)') as overtime,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Other Allowance (ሌላ አበል)') as oa,
				((select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)')+(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Overtime (ተጨማሪ ሰአት)')+(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Other Allowance (ሌላ አበል)')) as tax_able_amount,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Income Tax (የገቢ ግብር)') as tax_withheld,
				"" as cost_sahring
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
				where
					ss.start_date = '{0}';
				""".format(filters['start_date']))
		return res
	elif 'end_date' in filters:
		res = frappe.db.sql("""
				Select
				c.employer_tax_account,
				c.employer_enterprise_no,
				emp.tin_no,
				emp.employee_name,
				ss.start_date,
				ss.end_Date,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)') as basic,
				"" as total_transportation_allowance,
				"" as total_transportation_allowance,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Overtime (ተጨማሪ ሰአት)') as overtime,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Other Allowance (ሌላ አበል)') as oa,
				((select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)')+(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Overtime (ተጨማሪ ሰአት)')+(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Other Allowance (ሌላ አበል)')) as tax_able_amount,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Income Tax (የገቢ ግብር)') as tax_withheld,
				"" as cost_sahring
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
				where
					ss.end_date = '{0}';
				""".format(filters['end_date']))
		return res
	if 'start_date' in filters and 'end_date' in filters:
		res = frappe.db.sql("""
				Select
				c.employer_tax_account,
				c.employer_enterprise_no,
				emp.tin_no,
				emp.employee_name,
				ss.start_date,
				ss.end_Date,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)') as basic,
				"" as total_transportation_allowance,
				"" as total_transportation_allowance,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Overtime (ተጨማሪ ሰአት)') as overtime,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Other Allowance (ሌላ አበል)') as oa,
				((select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)')+(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Overtime (ተጨማሪ ሰአት)')+(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Other Allowance (ሌላ አበል)')) as tax_able_amount,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Income Tax (የገቢ ግብር)') as tax_withheld,
				"" as cost_sahring
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
				where
					ss.start_date = '{0}' and ss.end_date = '{1}';
				""".format(filters['start_date'], filters['end_date']))
		return res
	else:
		res = frappe.db.sql("""
				Select
				c.employer_tax_account,
				c.employer_enterprise_no,
				emp.tin_no,
				emp.employee_name,
				ss.start_date,
				ss.end_Date,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)') as basic,
				"" as total_transportation_allowance,
				"" as total_transportation_allowance,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Overtime (ተጨማሪ ሰአት)') as overtime,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Other Allowance (ሌላ አበል)') as oa,
				((select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Basic (መሰረዊ)')+(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Overtime (ተጨማሪ ሰአት)')+(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Other Allowance (ሌላ አበል)')) as tax_able_amount,
				(select amount from `tabSalary Detail` where parent=ss.name and emp.name = ss.employee and salary_component='Income Tax (የገቢ ግብር)') as tax_withheld,
				"" as cost_sahring
				from
					`tabEmployee` as emp
				join
					`tabSalary Slip` as ss
				on
					emp.name = ss.employee
				join 
					`tabCompany` as c
				on
					ss.company = c.name;
				""")
		return res