// Copyright (c) 2016, Atriina and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Withholding Tax Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __('From Date'),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_start_date"),
		},
		{
			"fieldname":"to_date",
			"label": __('To Date'),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_end_date"),
		},
		{
			"label": "From No",
			"fieldtype": 'Int',
			"fieldname": "from_no"
		},
		{
			"label": "To No",
			"fieldtype": "Int",
			"fieldname": 'to_no'
		}
	]
};
