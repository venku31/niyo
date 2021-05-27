from __future__ import unicode_literals
import frappe

def execute():
    leave_type = frappe.db.get_list("Leave Type",as_list=1)
    leave_type_list = []
    for i in leave_type:
        for j in i:
            leave_type_list.append(j)
            
    if "Maternity Leave" not in leave_type_list:
        print("========= inside if =========")
        doc = frappe.get_doc({
            'doctype': 'Leave Type',
            'leave_type_name': 'Maternity Leave'
        })
        doc.insert()
        doc.save()