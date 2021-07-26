import frappe

def execute():
    try:
        frappe.delete_doc('DocType', 'Import PO')
        frappe.db.sql("""
        drop table `tabImport PO`;
        """) 
    except Exception:
        pass
    try:
        frappe.delete_doc('DocType', 'Import PO Item')
        frappe.db.sql("""
        drop table `tabImport PO Item`;
        """)
    except Exception:
        pass
    try:
        frappe.delete_doc('DocType', 'Payroll Setting')
        frappe.db.sql("""
        drop table `tabPayroll Setting`;
        """)
    except Exception:
        pass

    frappe.db.commit()
