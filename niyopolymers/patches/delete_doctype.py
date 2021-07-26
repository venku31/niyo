import frappe

def execute():
        frappe.delete_doc('DocType', 'Import PO', delete_permanently=True)
        frappe.db.sql("""
        drop table `tabImport PO`;
        """) 
        frappe.delete_doc('DocType', 'Import PO Item', delete_permanently=True)
        frappe.db.sql("""
        drop table `tabImport PO Item`;
        """)
        frappe.delete_doc('DocType', 'Payroll Setting', delete_permanently=True)
        frappe.db.sql("""
        drop table `tabPayroll Setting`;
        """)

    frappe.db.commit()
