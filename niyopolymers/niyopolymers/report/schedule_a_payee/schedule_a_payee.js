// Copyright (c) 2016, Atriina and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Schedule a Payee"] = {
	"filters": [
		{
			"fieldname":"start_date",
			"label": __('Start Date'),
			"fieldtype": "Date",
		},
		{
			"fieldname":"end_date",
			"label": __('End Date'),
			"fieldtype": "Date",
		},
	]
};