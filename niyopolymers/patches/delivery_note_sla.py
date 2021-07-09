import frappe

def execute():
   if frappe.db.exists("Custom Field","Delivery Note-service_level_agreement"):
       frappe.db.delete('Custom Field', {'fieldname': 'service_level_agreement'})
       frappe.db.commit()


        
