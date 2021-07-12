// Copyright (c) 2021, Atriina and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shift Production', {
	// refresh: function(frm) {

	// }
});
cur_frm.fields_dict.supervisor.get_query = function(doc) {
 	return {
 		filters: {
			designation: "Reporting Manager" 
			}
 	}
 }
frappe.ui.form.on('Shift Production Details', {
	blowing:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var blowing = (flt(d.counter_end) - flt(d.counter_start));
		frappe.model.set_value(cdt, cdn, "blowing", blowing);
		},
	counter_start:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
    	var blowing = (flt(d.counter_end) - flt(d.counter_start));
		frappe.model.set_value(cdt, cdn, "blowing", blowing);
	var blowing_perform = (flt(d.blowing) - flt(d.rejection)-flt(d.hot)-flt(d.white));
                frappe.model.set_value(cdt, cdn, "blowing_perform", blowing_perform);

	},
	counter_end:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var blowing = (flt(d.counter_end) - flt(d.counter_start));
		frappe.model.set_value(cdt, cdn, "blowing", blowing);
		var blowing_perform = (flt(d.blowing) - flt(d.rejection)-flt(d.hot)-flt(d.white));
                frappe.model.set_value(cdt, cdn, "blowing_perform", blowing_perform);

	},
		rejection:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var blowing_perform = (flt(d.blowing) - flt(d.rejection)-flt(d.hot)-flt(d.white));
		frappe.model.set_value(cdt, cdn, "blowing_perform", blowing_perform);
	},
		white:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var blowing_perform = (flt(d.blowing) - flt(d.rejection)-flt(d.hot)-flt(d.white));
		frappe.model.set_value(cdt, cdn, "blowing_perform", blowing_perform);
	},
	    hot:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var blowing_perform = (flt(d.blowing) - flt(d.rejection)-flt(d.hot)-flt(d.white));
		frappe.model.set_value(cdt, cdn, "blowing_perform", blowing_perform);
	},
	validate:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var blowing = (flt(d.counter_end) - flt(d.counter_start));
		frappe.model.set_value(cdt, cdn, "blowing", blowing);	
	    var blowing_perform = ((flt(d.counter_end) - flt(d.counter_start)) - flt(d.rejection)-flt(d.hot)-flt(d.white));
		frappe.model.set_value(cdt, cdn, "blowing_perform", blowing_perform);	
	}
})
