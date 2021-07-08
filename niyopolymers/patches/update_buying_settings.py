import frappe

def execute():
    buying_settings = frappe.get_single("Buying Settings")

    buying_settings.update(
        {
            'allow_multiple_items': 1,
            'backflush_raw_materials_of_subcontract_based_on': 'Material Transferred for Subcontract',
            'buying_price_list': 'Standard Buying',
            'maintain_same_rate': 1,
            'over_transfer_allowance': 0,
            'po_required': 'No',
            'pr_required': 'No',
            'supp_master_name': "Supplier Name"
        }
    )
    buying_settings.save()
    frappe.db.commit()