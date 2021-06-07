// login.js
// don't remove this line (used in test)

window.disable_signup = {{ disable_signup and "true" or "false" }};

window.login = {};

window.verify = {};

{% include 'frappe/templates/includes/login/login.js' %};

login.login_handlers = (function() {
	var get_error_handler = function(default_message) {
		return function(xhr, data) {
			if(xhr.responseJSON) {
				data = xhr.responseJSON;
			}

			var message = default_message;
			if (data._server_messages) {
				message = ($.map(JSON.parse(data._server_messages || '[]'), function(v) {
					// temp fix for messages sent as dict
					try {
						return JSON.parse(v).message;
					} catch (e) {
						return v;
					}
				}) || []).join('<br>') || default_message;
			}

			if(message===default_message) {
				login.set_indicator(message, 'red');
			} else {
				login.reset_sections(false);
			}

		};
	}

	var login_handlers = {
		200: function(data) {
			if(data.message == 'Logged In'){
				console.log('on login')
				login.set_indicator('{{ _("Success") }}', 'green');
                // window.location.href = frappe.utils.get_url_arg("redirect-to") || data.home_page;
                window.location.href = "/desk#List/ToDo/List"
			} else if(data.message == 'Password Reset'){
				window.location.href = data.redirect_to;
			} else if(data.message=="No App") {
				login.set_indicator("{{ _("Success") }}", 'green');
				if(localStorage) {
					var last_visited =
						localStorage.getItem("last_visited")
						|| frappe.utils.get_url_arg("redirect-to");
					localStorage.removeItem("last_visited");
				}

				if(data.redirect_to) {
					window.location.href = data.redirect_to;
				}

				if(last_visited && last_visited != "/login") {
					window.location.href = last_visited;
				} else {
					window.location.href = data.home_page;
				}
			} else if(window.location.hash === '#forgot') {
				if(data.message==='not found') {
					login.set_indicator('{{ _("Not a valid user") }}', 'red');
				} else if (data.message=='not allowed') {
					login.set_indicator('{{ _("Not Allowed") }}', 'red');
				} else if (data.message=='disabled') {
					login.set_indicator('{{ _("Not Allowed: Disabled User") }}', 'red');
				} else {
					login.set_indicator('{{ _("Instructions Emailed") }}', 'green');
				}


			} else if(window.location.hash === '#signup') {
				if(cint(data.message[0])==0) {
					login.set_indicator(data.message[1], 'red');
				} else {
					login.set_indicator('{{ _("Success") }}', 'green');
					frappe.msgprint(data.message[1])
				}
				//login.set_indicator(__(data.message), 'green');
			}

			//OTP verification
			if(data.verification && data.message != 'Logged In') {
				login.set_indicator('{{ _("Success") }}', 'green');

				document.cookie = "tmp_id="+data.tmp_id;

				if (data.verification.method == 'OTP App'){
					continue_otp_app(data.verification.setup, data.verification.qrcode);
				} else if (data.verification.method == 'SMS'){
					continue_sms(data.verification.setup, data.verification.prompt);
				} else if (data.verification.method == 'Email'){
					continue_email(data.verification.setup, data.verification.prompt);
				}
			}
		},
		401: get_error_handler('{{ _("Invalid Login. Try again.") }}'),
		417: get_error_handler('{{ _("Oops! Something went wrong") }}')
	};

	return login_handlers;
} )();