import frappe

def execute():
    website_settings = frappe.get_single("Website Settings")

    website_settings.update(
        {
            'home_page': 'login',
            'website_theme': 'Standard'
        }
    )
    website_settings.save()
    frappe.db.commit()