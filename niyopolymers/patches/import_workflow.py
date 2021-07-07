import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "workflow.csv")
    frappe.core.doctype.data_import.data_import.import_file("Workflow", path, "Insert", console=True)