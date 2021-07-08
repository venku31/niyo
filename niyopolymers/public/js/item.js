function updateUOM(frm) {
    var itemDocument = frm.doc


    if (frm.doc.uoms.length < "2") {

        let d = frm.add_child("uoms");
        d.uom = "Nos";
        d.conversion_factor = itemDocument.standard_weight;
        refresh_field("uoms");

    }
    else {
        frm.doc.uoms[1].conversion_factor = itemDocument.standard_weight;

        refresh_field("uoms");


    }



}


function weight(frm) {
    var a = frm.doc;
    if (a.diameter !== 0 && a.thickness !== 0) {
        var w = 3.14 * (a.diameter / 2) * (a.diameter / 2) * a.thickness * (2700 / 1000000000);
        frm.set_value('standard_weight', w);
    }
    if (a.diameter === 0 || a.thickness === 0) {
        frm.set_value('standard_weight', '0');

    }
}




frappe.ui.form.on('Item', {
    diameter: function (frm) {
        weight(frm)
    }

});

frappe.ui.form.on('Item', {
    thickness: function (frm) {
        weight(frm)
        refresh_field("standard_weight");
    }

});

frappe.ui.form.on('Item', {
    standard_weight: function (frm) {
        updateUOM(frm);
    }


});
