import frappe

def execute():
    company = frappe.get_doc("Company", 'Niyo Polymers')

    company.update(
        {
            'company_name': "Niyo Polymers",
            'credit_limit': 0,
            'date_of_establishment': "2011-10-22",
            'default_holiday_list': "Niyo Holidays",
            'enable_perpetual_inventory': 0,
            'tax_id': "0020338046",
        }
    )
    company.save()
    frappe.db.commit()