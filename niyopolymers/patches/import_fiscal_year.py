import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "fiscal_year.csv")
    frappe.core.doctype.data_import.data_import.import_file("Fiscal Year", path, "Insert", console=True)