import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "designation.csv")
    frappe.core.doctype.data_import.data_import.import_file("Designation", path, "Insert", console=True)