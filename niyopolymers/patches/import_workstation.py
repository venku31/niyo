import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "workstation.csv")
    frappe.core.doctype.data_import.data_import.import_file("Workstation", path, "Insert", console=True)