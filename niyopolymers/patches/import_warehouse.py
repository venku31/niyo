import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "warehouse.csv")
    frappe.core.doctype.data_import.data_import.import_file("Warehouse", path, "Insert", console=True)