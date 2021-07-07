import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "bom.csv")
    frappe.core.doctype.data_import.data_import.import_file("BOM", path, "Insert", console=True)