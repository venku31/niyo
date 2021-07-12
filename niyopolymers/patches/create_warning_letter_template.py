import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "warning_letter_template.csv")
    frappe.core.doctype.data_import.data_import.import_file("Warning Letter Template", path, "Insert", console=True)