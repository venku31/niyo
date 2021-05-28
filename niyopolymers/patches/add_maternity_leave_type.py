from __future__ import unicode_literals
import frappe

def execute():
    doc = frappe.get_doc({
        'doctype': 'Leave Type',
        'leave_type_name': 'Maternity Leave'
    })
    doc.insert()