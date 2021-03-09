frappe.listview_settings['Employee'] = {
	add_fields: ["warnings_letters_given"],
	get_indicator: function(doc) {
		if(doc.warnings_letters_given == '1'){
            return [__("1"), "green", "warnings_letters_given,=,1"];
        }
        if(doc.warnings_letters_given == '2'){
            return [__("2"), "orange", "warnings_letters_given,=,2"];
        }
        if(doc.warnings_letters_given == '3'){
            return [__("3"), "red", "warnings_letters_given,=,3"];
        }
	}
};