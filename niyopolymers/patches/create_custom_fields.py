import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
	custom_fields = {
		'Selling Settings': [
			dict(fieldname='last_fs_number', fieldtype='Data', insert_after='hide_tax_id',
				label='Last FS Number')
		]
	}
	create_custom_fields(custom_fields)