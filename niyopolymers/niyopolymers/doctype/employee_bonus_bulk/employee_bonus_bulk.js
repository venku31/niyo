// Copyright (c) 2021, Atriina and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Bonus Bulk', {
	refresh: function(frm) {
		if (frm.doc.docstatus == 0) {
			if(!frm.is_new()) {
				// frm.page.clear_primary_action();
				frm.add_custom_button(__("Get Employees"),
					function() {
						frm.events.get_employee_details(frm);
					}
				).toggleClass('btn-primary', !(frm.doc.employee_details || []).length);
			}
		}
	},
	get_employee_details: function (frm) {
		return frappe.call({
			doc: frm.doc,
			method: 'fill_employee_details',
			callback: function(r) {
				console.log(r)
				if (r.docs[0].employees){
					frm.save();
					frm.refresh();
				}
			}
		})
	},
});
