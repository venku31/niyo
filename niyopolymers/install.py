import frappe

def remove_patches_entries_and_migrate():
    frappe.db.sql("DELETE FROM `tabPatch Log` WHERE patch LIKE %s", ("ethal.patches.%"))
    frappe.db.commit()
    site_name = frappe.utils.get_site_base_path().replace("./", "")
    frappe.commands.popen("bench --site {} migrate".format(site_name))

def after_install():
    remove_patches_entries_and_migrate()
    frappe.db.commit()