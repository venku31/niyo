import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "department.csv")
    frappe.core.doctype.data_import.data_import.import_file("Department", path, "Insert", console=True)