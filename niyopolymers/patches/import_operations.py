import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "operation.csv")
    frappe.core.doctype.data_import.data_import.import_file("Operation", path, "Insert", console=True)