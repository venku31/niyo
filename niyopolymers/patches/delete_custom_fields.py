import frappe

def execute():
    try:
        frappe.db.sql("""
        delete from `tabCustom Field` where name = 'Delivery Note-total_net_weight_aluminium';
        """)
        frappe.db.sql("""
        delete from `tabCustom Field` where name = 'Delivery Note-total_net_weight_weigh_bridge';
        """)
    except frappe.DuplicateEntryError:
        pass

    frappe.db.commit()
