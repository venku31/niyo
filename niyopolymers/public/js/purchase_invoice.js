frappe.ui.form.on('Purchase Invoice', {
    before_save:function(frm){
        if(frm.doc.withholding_category == "Purchase"){
		    if(frm.doc.total <= 10000){
		        frm.set_value('taxes_and_charges','Vat @15% - NP')
		    }
		    if(frm.doc.total > 10000){
		        if(frm.doc.tax_id){
		            frm.set_value('taxes_and_charges','Vat @15% + Wht 2% - NP')
		            
		        }
		        else{
		            frm.set_value('taxes_and_charges','Vat @15% + Wht 30% - NP')
		            
		        }
		    }
		}
		else{
		    if(frm.doc.total < 3000){
		        frm.set_value('taxes_and_charges','Vat @15% - NP')
		    }
		    if(frm.doc.total > 3000){
		        if(frm.doc.tax_id){
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
            name: frm.doc.taxes_and_charges,
        },
        callback(response) {
            if(response.message) {
                var template = response.message;
                cur_frm.set_value("taxes",template.taxes)
            }
			else{
				frappe.throw("Invalid Purchase Taxes and Charges Template")
			}
        }
    });
	}
})