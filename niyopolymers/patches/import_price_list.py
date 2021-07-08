import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "price_list.csv")
    frappe.core.doctype.data_import.data_import.import_file("Price List", path, "Insert", console=True)