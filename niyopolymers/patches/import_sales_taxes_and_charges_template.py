import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "sales_taxes_and_charges_template.csv")
    frappe.core.doctype.data_import.data_import.import_file("Sales Taxes and Charges Template", path, "Insert", console=True)