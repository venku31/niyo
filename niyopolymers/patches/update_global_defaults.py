import frappe

def execute():
    global_defaults = frappe.get_single("Global Defaults")

    global_defaults.update(
        {
            'country': 'Ethiopia',
            'current_fiscal_year': '2020',
            'default_company': 'Niyo Polymers',
            'default_currency': 'ETB',
            'disable_in_words': 0,
            'disable_rounded_total': 1,
            'hide_currency_symbol': ''
        }
    )
    global_defaults.save()
    frappe.db.commit()