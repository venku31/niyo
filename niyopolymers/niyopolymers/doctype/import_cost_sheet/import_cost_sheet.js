// Copyright (c) 2021, Atriina and contributors
// For license information, please see license.txt

frappe.ui.form.on('Import Cost Sheet', {
	refresh: function(frm) {
		frm.set_query('grn', () => {
			return {
				filters: {
					docstatus: 1
				}
			}
		})
		frm.set_query('purchase_invoice', () => {
			return {
				filters: {
					docstatus: 1
				}
			}
		})
		frm.fields_dict['import_cost_sheet_items'].grid.get_field("purchase_invoice").get_query = function(doc, cdt, cdn) {
	        return{
	            filters: {
					docstatus: 1
				}
	        }
	    }
		if (frm.doc.import_cost_sheet_items == undefined) {
			var l = ['Sea Fright (ETB)', 'Inland Fright (ETB)', 'Insurance (ETB)', 'Import Customs Duty (ETB)', 'Other (ETB)', 'Bank charge (ETB)', 'Storage (ETB)', 'Port handling charge (ETB)', 'Transit and clearing (ETB)', 'Loading & unloading (ETB)', 'Inland transport (ETB)', 'Miscellaneous (ETB)']
			
			for (var i = 0; i < l.length; i++) {
				var childTable = cur_frm.add_child("import_cost_sheet_items");
				console.log(i)
				childTable.items = l[i]
			}
			cur_frm.refresh_fields("import_cost_sheet_items");
			}
		},
	// setup: function(frm){
	// 	if (frm.doc.import_cost_sheet_items == undefined) {
	// 	var l = ['Sea Fright (ETB)', 'Inland Fright (ETB)', 'Insurance (ETB)', 'Import Customs Duty (ETB)', 'Other (ETB)', 'Bank charge (ETB)', 'Storage (ETB)', 'Port handling charge (ETB)', 'Transit and clearing (ETB)', 'Loading & unloading (ETB)', 'Inland transport (ETB)', 'Miscellaneous (ETB)']
		
	// 	for (var i = 0; i < l.length; i++) {
	// 		var childTable = cur_frm.add_child("import_cost_sheet_items");
	// 		console.log(i)
	// 		childTable.items = l[i]
	// 	}
	// 	cur_frm.refresh_fields("import_cost_sheet_items");
	// 	}
	// },
	grn: function(frm){
		if (frm.doc.grn){
			frm.clear_table("import_cost_sheet_details"); 
			frm.refresh_field('import_cost_sheet_details');
			frappe.call({
				method:"niyopolymers.niyopolymers.doctype.import_cost_sheet.import_cost_sheet.get_value",
				args: {
				name: frm.doc.grn
				}
			})
			.success(success => {
			var total_amount = 0
			for (var i=0; i<success.message.length; i++){
				total_amount += success.message[i].amount
			}
			for (var i=0; i<success.message.length; i++){
				let row = frm.add_child('import_cost_sheet_details')
				row.item_code= success.message[i].item_code
				row.qty = success.message[i].qty
			}
			frm.refresh_field('import_cost_sheet_details');
			})
		}
	}
});
