import frappe

def execute():
    accounts_settings = frappe.get_single("Accounts Settings")

    accounts_settings.update(
        {
            'add_taxes_from_item_tax_template': 1,
            'allow_stale': 1,
            'auto_accounting_for_stock': 1,
            'automatically_fetch_payment_terms': 0,
            'book_asset_depreciation_entry_automatically': 1,
            'check_supplier_invoice_uniqueness': 0,
            'determine_address_tax_category_from': 'Billing Address',
            'make_payment_via_journal_entry': 0,
            'over_billing_allowance': 0,
            'show_inclusive_tax_in_print': 0,
            'show_payment_schedule_in_print': 0,
            'stale_days': 1,
            'unlink_advance_payment_on_cancelation_of_order': 1,
            'unlink_payment_on_cancellation_of_invoice': 1,
            'use_custom_cash_flow': 0
        }
    )
    accounts_settings.save()
    frappe.db.commit()