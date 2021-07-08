import frappe

def execute():
    roles = ['CRV Approver', 'Deputy PRA Approver', 'Face Recognition User', "Journal Entry Approver", 'Material Request Approver', 'Payment Entry Approver', 'PCPV Approver', 'PRA Approver', 'PRA Checker', 'Purchase Invoice Approver', 'Purchase Order Approver', 'Report Manager', 'Sales Order Approver', 'Sales Invoice Approver']
    for role in roles:
        try:
            frappe.get_doc({
                'doctype': 'Role',
                'role_name': role
            }).insert()
        except frappe.DuplicateEntryError:
            pass

    frappe.db.commit()
