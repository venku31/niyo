import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "salary_component.csv")
    frappe.core.doctype.data_import.data_import.import_file("Salary Component", path, "Insert", console=True)