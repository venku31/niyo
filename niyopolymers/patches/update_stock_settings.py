import frappe

def execute():
    stock_settings = frappe.get_single("Stock Settings")

    stock_settings.update(
        {
            'action_if_quality_inspection_is_not_submitted': 'Stop',
            'allow_negative_stock': 0,
            'auto_indent': 1,
            'auto_insert_price_list_rate_if_missing': 1,
            'automatically_set_serial_nos_based_on_fifo': 1,
            'clean_description_html': 1,
            'default_warehouse': 'Stores - NP',
            'item_naming_by': 'Item Code',
            'naming_series_prefix': 'BATCH-',
            'over_delivery_receipt_allowance': 0,
            'reorder_email_notify': 0,
            'set_qty_in_transactions_based_on_serial_no_input': 1,
            'show_barcode_field': 1,
            'stock_frozen_upto_days': 0,
            'stock_uom': 'Nos',
            'use_naming_series': 0,
            'valuation_method': "FIFO"
        }
    )
    stock_settings.save()
    frappe.db.commit()