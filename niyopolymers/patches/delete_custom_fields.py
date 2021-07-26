import frappe

def execute():
        frappe.db.sql("""
        delete from `tabCustom Field` where name = 'Delivery Note-total_net_weight_aluminium';
        """)
        frappe.db.sql("""
        delete from `tabCustom Field` where name = 'Delivery Note-total_net_weight_weigh_bridge';
        """)

    frappe.db.commit()
