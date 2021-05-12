// Copyright (c) 2016, Atriina and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Attentance Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Datetime",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname":"shift",
			"label":__("Shift"),
			"fieldtype": "Link",
			"options": "Shift Type"
		}
	]
};
