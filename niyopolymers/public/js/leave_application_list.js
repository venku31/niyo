frappe.listview_settings['Leave Application'] = {
    onload(listview) {
        listview.page.add_menu_item(__("Leave Mail"), function() {
            frappe.call({
                method: "niyopolymers.hr.maternity_leave_mail",
                callback: function(r) {
                    console.log("in callback after leave mail triggered ")
                }
            })
        })
    },
}