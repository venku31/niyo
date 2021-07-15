// Copyright (c) 2016, Atriina and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Missed Delivery Note"] = {
	"filters": [
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
