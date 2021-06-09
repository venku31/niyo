frappe.ui.form.on('Purchase Invoice', {
    before_save:function(frm){
        if(cur_frm.doc.withholding_category == "Purchase"){
		    if(frm.doc.total <= 10000){
		        console.log("Hello")
		        cur_frm.set_value('taxes_and_charges','Vat @15% - NP')
		    }
		    if(frm.doc.total > 10000){
		        if(cur_frm.doc.tax_id){
		            cur_frm.set_value('taxes_and_charges','Vat @15% + Wht 2% - NP')
		            
		        }
		        else{
		            cur_frm.set_value('taxes_and_charges','Vat @15% + Wht 30% - NP')
		            
		        }
		    }
		}
		if(cur_frm.doc.withholding_category == "Service"){
		    if(frm.doc.total < 3000){
		        frm.set_value('taxes_and_charges','Vat @15% - NP')
		    }
		    if(frm.doc.total > 3000){
		        if(cur_frm.doc.tax_id){
		            frm.set_value('taxes_and_charges','Vat @15% + Wht 2% - NP')
		        }
		        else{
		            frm.set_value('taxes_and_charges','Vat @15% + Wht 30% - NP')
		        }
		    }
		}
		frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Purchase Taxes and Charges Template",
            name: cur_frm.doc.taxes_and_charges,
        },
        callback(r) {
            if(r.message) {
                var task = r.message;
                cur_frm.set_value("taxes",task.taxes)
            }
        }
    });
	}
})