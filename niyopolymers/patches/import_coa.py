import frappe
from erpnext.accounts.doctype.chart_of_accounts_importer.chart_of_accounts_importer import import_coa

def execute():
    path = frappe.get_app_path("niyopolymers", "patches", "imports", "coa.csv")
    
    csv_file = open(path, 'r')
    csv_content = csv_file.read()
    csv_file.close()

    f = frappe.new_doc('File')
    f.file_name = 'coa.csv'
    f.content = csv_content
    f.insert()
    frappe.db.commit()

    import_coa(f.file_url, 'Niyo Polymers')
    f.delete()
    frappe.db.commit()
