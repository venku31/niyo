import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "territory.csv")
    frappe.core.doctype.data_import.data_import.import_file("Territory", path, "Insert", console=True)