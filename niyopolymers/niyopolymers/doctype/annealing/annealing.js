// Copyright (c) 2021, Atriina and contributors
// For license information, please see license.txt

frappe.ui.form.on('Annealing', {
	date: function(frm) {
		if (frm.doc.date) {
			frappe.call({
				'method': 'niyopolymers.niyopolymers.doctype.annealing.annealing.set_day_and_month_of_date',
				'args': {
					'doc': frm.doc
				}
			})
			.success(success => {
				console.log(success)
				frm.set_value('day', success.message[0])
				frm.set_value('month', success.message[1])
			})
		}	
	}
});
