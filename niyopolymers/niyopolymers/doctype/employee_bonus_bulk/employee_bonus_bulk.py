# -*- coding: utf-8 -*-
# Copyright (c) 2021, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class EmployeeBonusBulk(Document):

	def on_submit(self):
		employees = frappe.db.get_all('Bonus Employee Details', {'parent': self.name}, ['employee','employee_name','bonus'], as_list = 1)
		print("on submit employees ==> ",employees)
		if employees:
			for e in employees:
				additional_salary = frappe.db.exists('Additional Salary', {
						'employee': e[0], 
						'salary_component': 'Bonus',
						'payroll_date': self.bonus_date, 
						'company': frappe.db.get_value('Employee', e[0], 'company'),
						'docstatus': 1
					})
				if not additional_salary:
					additional_salary = frappe.new_doc('Additional Salary')
					additional_salary.employee = e[0]
					additional_salary.salary_component = 'Bonus'
					additional_salary.amount = e[2]
					additional_salary.payroll_date = self.bonus_date
					additional_salary.company = frappe.db.get_value('Employee', e[0], 'company')
					additional_salary.submit()

	def on_cancel(self):
		employees = frappe.db.get_all('Bonus Employee Details', {'parent': self.name}, ['employee','employee_name','bonus'], as_list = 1)
		if employees:
			for i in employees:
				filters = {
				'employee':i[0],
				'salary_component':'Bonus',
				'payroll_date' : self.bonus_date,
				'amount': i[2]
			}
				incentive_removed = frappe.db.get_value('Additional Salary',filters, 'name')
				if incentive_removed:
					frappe.get_doc('Additional Salary', incentive_removed).cancel()
					frappe.db.commit()
	
	def fill_employee_details(self):
		self.set('employee_details', [])
		employees = self.get_emp_list()

	def get_emp_list(self):
		employees = frappe.db.sql("""
		select employee_name from `tabAttendance` where 
		status = "Present" and docstatus = 1 group by employee_name having count(employee_name) >= 75""")

		employees = [item for elem in employees for item in elem]

		sal_lst = []
		for i in employees:
			sal = frappe.db.sql("""
			select a.employee, a.employee_name, sum(b.amount) from `tabSalary Slip` as a inner join `tabSalary Detail`
			 as b on a.name = b.parent  where b.parenttype = "Salary Slip" and b.parentfield = "earnings"
			  and b.salary_component = "Basic (መሰረዊ)" and a.employee_name = %s and a.start_date > %s and a.end_date <= %s;
			""",(i,self.cycle_from_date,self.cycle_to_date))
			for i in sal:
				sal_lst.append(i)

		emp_and_bonus= []
		for i in sal_lst:
			my_dict = {"employee":i[0],"employee_name":i[1],"bonus":i[2]}
			self.append('employees',my_dict)

			

			

	