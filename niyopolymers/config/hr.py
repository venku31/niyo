from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			'label': _('Payroll'),
			'items': [
				{ 'type': 'doctype', 'name': 'Employee Incentive Bulk', "onboard": 1 }
			]
		},
		{
			'label': _('Custom Reports'),
			'items': [
				{
					'type': 'report', 'label': _('Daily Checkins'), 'name': 'Daily Attentance Report', 'onboard': 1, 'route': 'query-report/Daily Checkins'
				}
			]
		}
	]
