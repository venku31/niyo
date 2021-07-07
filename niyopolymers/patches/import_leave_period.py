import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "leave_period.csv")
    frappe.core.doctype.data_import.data_import.import_file("Leave Period", path, "Insert", console=True)