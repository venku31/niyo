import frappe

def execute():
    try:
        frappe.db.sql("""
        drop table `tabImport PO`;
        """)
    except frappe.DuplicateEntryError:
        pass
    try:    
        frappe.db.sql("""
        drop table `tabImport PO Item`;
        """)
    except frappe.DuplicateEntryError:
        pass
    try:
        frappe.db.sql("""
        drop table `tabPayroll Setting`;
        """)
    except frappe.DuplicateEntryError:
        pass

    frappe.db.commit()
