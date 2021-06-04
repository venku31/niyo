frappe.listview_settings['Attendance'] = {
    onload: function(listview) {
		this.add_button('Consecutive Leaves', "default", function() { 
            frappe.call({
                method: "niyopolymers.hr.trigger_mail_if_absent_consecutive_5_days"
             })
             .success(success => {
                 console.log(success.message)
             })
        })
	},

	add_button(name, type, action, wrapper_class=".page-actions") {
		const button = document.createElement("button");
		button.classList.add("btn", "btn-" + type, "btn-sm", "ml-2");
		button.innerHTML = name;
		button.onclick = action;
		document.querySelector(wrapper_class).prepend(button);
	},
}