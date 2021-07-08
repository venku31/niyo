import frappe

def execute():
    selling_settings = frappe.get_single("Selling Settings")

    selling_settings.update(
        {
            'allow_against_multiple_purchase_orders': 0,
            'allow_multiple_items': 1,
            'close_opportunity_after_days': 15,
            'cust_master_name': 'Customer Name',
            'customer_group': 'All Customer Groups',
            'dn_required': 'No',
            'editable_price_list_rate': 0,
            'hide_tax_id': 0,
            'maintain_same_sales_rate': 0,
            'sales_update_frequency': 'Each Transaction',
            'selling_price_list': 'Standard Selling',
            'so_required': 'No',
            'territory': 'All Territories',
            'validate_selling_price': 0
        }
    )
    selling_settings.save()
    frappe.db.commit()