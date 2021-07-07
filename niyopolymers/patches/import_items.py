import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "item.csv")
    frappe.core.doctype.data_import.data_import.import_file("Item", path, "Insert", console=True)