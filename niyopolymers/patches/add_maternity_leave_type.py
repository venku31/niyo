from __future__ import unicode_literals
import frappe

def execute():
    try:
        doc = frappe.get_doc({
            'doctype': 'Leave Type',
            'leave_type_name': 'Maternity Leave'
        })
        doc.insert()
        frappe.db.commit()
    except frappe.DuplicateEntryError:
        pass
