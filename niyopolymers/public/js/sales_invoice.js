frappe.ui.form.on('Sales Invoice', {	
	after_workflow_action: function(frm){
	    if (frm.doc.docstatus == 1) {
			frappe.call({
				method: "erpnext.accounts.doctype.payment_entry.payment_entry.get_payment_entry",
				args: {
					"dt": frm.doc.doctype,
					"dn": frm.doc.name
				},
				callback: function(r) {
					var doclist = frappe.model.sync(r.message);
					frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
					// cur_frm.refresh_fields()
				}
	    	});
		}
	}
});