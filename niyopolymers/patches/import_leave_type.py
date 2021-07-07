import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "leave_type.csv")
    frappe.core.doctype.data_import.data_import.import_file("Leave Type", path, "Insert", console=True)