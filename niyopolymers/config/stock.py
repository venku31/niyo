from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			'label': _('Stock Transactions'),
			'items': [
				{ 'type': 'doctype', 'name': 'Shift Production', "onboard": 1 }
			]
		}
    ]