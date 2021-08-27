frappe.ui.form.on('Purchase Invoice', {
	bill_no: function (frm) {
		var a = frm.doc.bill_no;
		var mystr = a.replace(/\D/g, '');
		frm.set_value('bill_no', mystr);
		frm.refresh_field('bill_no')
	}
});

frappe.ui.form.on('Purchase Invoice', {
	withholding_receipt_no: function (frm) {
		var a = frm.doc.withholding_receipt_no;
		var mystr = a.replace(/\D/g, '');
		frm.set_value('withholding_receipt_no', mystr);
		frm.refresh_field('withholding_receipt_no')
	},
	refresh: function (frm) {
		frm.fields_dict['items'].grid.get_field("expense_account").get_query = function (doc, cdt, cdn) {
			return {
				filters: [
					['Account', 'is_group', '=', 'No'],
					['Account', 'company', '=', frm.doc.company]
				]
			}
		}
	},
})
frappe.ui.form.on('Purchase Invoice', {
	validate: function (frm) {
		calculate_taxes_and_charges(frm)
	}
});

function calculate_taxes_and_charges(frm) {
	console.log("calculating taxes and charges")
	if (!frm.doc.withholding_category && !cur_frm.doc.total && !frm.doc.tax_id) {
		console.log("was here")
		return
	}
	let taxes_and_charges = null
	let threshold = frm.doc.withholding_category == "Purchase" ? 10000 : 3000
	if (frm.doc.total <= threshold) {
		taxes_and_charges = 'Vat @15% - NP'
	}
	else {
		taxes_and_charges = frm.doc.tax_id ? 'Vat @15% + Wht 2% - NP' : 'Vat @15% + Wht 30% - NP'
	}
	frm.set_value("taxes_and_charges", taxes_and_charges)
	frm.refresh_field("taxes_and_charges")
	console.log(frm.doc.taxes_and_charges)
	console.log("Leaving taxes and charges")
	frm.trigger("taxes_and_charges")
}