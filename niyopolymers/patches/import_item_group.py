import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "item_group.csv")
    frappe.core.doctype.data_import.data_import.import_file("Item Group", path, "Insert", console=True)