import frappe

def execute():
    frappe.delete_doc('Custom Field', 'Delivery Note-total_net_weight_aluminium')
   
    frappe.delete_doc('Custom Field', 'Delivery Note-total_net_weight_weigh_bridge')

    frappe.db.commit()