import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "role.csv")
    frappe.core.doctype.data_import.data_import.import_file("Role", path, "Insert", console=True)