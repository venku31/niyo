frappe.listview_settings['Salary Structure Assignment'] = {
    add_fields: ["promotion"],
    get_indicator: function(doc) {
        if(doc.promotion=="Salary Updated") {
            return [__("Salary Updated"), "green", "promotion,=,Salary Updated"];
        }
    }
}