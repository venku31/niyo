import frappe

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "email_account.csv")
    frappe.core.doctype.data_import.data_import.import_file("Email Account", path, "Insert", console=True)