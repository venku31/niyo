// Copyright (c) 2016, Atriina and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Consoliadated Report"] = {
	"filters": [
		{
			"label": __("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link", 
			"options": "Employee",
			"reqd": 1
		}
	]
};
