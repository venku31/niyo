import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "salary_structure.csv")
    frappe.core.doctype.data_import.data_import.import_file("Salary Structure", path, "Insert", console=True)