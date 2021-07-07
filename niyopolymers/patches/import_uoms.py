import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "uom.csv")
    frappe.core.doctype.data_import.data_import.import_file("UOM", path, "Insert", console=True)