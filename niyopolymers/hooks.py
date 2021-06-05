# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "niyopolymers"
app_title = "Niyopolymers"
app_publisher = "Atriina"
app_description = "IDK"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "deverlopers@atriina.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/css/world-calendar.min.css"
app_include_js = "/assets/js/world-calendar.min.js"

# include js, css files in header of web template
# web_include_css = "/assets/niyopolymers/css/niyopolymers.css"
# web_include_js = "/assets/niyopolymers/js/niyopolymers.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "niyopolymers.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "niyopolymers.install.before_install"
# after_install = "niyopolymers.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "niyopolymers.notifications.get_notification_config"

# get_rooms = 'frappe.chat.doctype.chat_room.chat_room.get_rooms'

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"niyopolymers.tasks.all"
# 	],
# 	"daily": [
# 		"niyopolymers.tasks.daily"
# 	],
# 	"hourly": [
# 		"niyopolymers.tasks.hourly"
# 	],
# 	"weekly": [
# 		"niyopolymers.tasks.weekly"
# 	]
# 	"monthly": [
# 		"niyopolymers.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "niyopolymers.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "niyopolymers.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "niyopolymers.task.get_dashboard_data"
# }

# on_session_creation = 'niyopolymers.hr.successful_login'

app_include_js = "/assets/niyopolymers/js/transaction.js"

doctype_js = {
    'Sales Invoice': 'public/js/sales_invoice.js',
}

doc_events = {
    "Payroll Entry": {
		"before_submit": "niyopolymers.hr.update_salary_structure_assignment_rate"
	},
	"Salary Slip": {
		"before_insert": "niyopolymers.hr.before_insert_salary_slip",
		"get_emp_and_leave_details": "niyopolymers.hr.before_save_salary_slip",
		"before_save": "niyopolymers.hr.before_save"
	},
	"Employee": {
		"on_update": "niyopolymers.hr.on_update_employee"
	},
	"Interview Configuration": {
        "before_save": "niyopolymers.niyopolymers.doctype.interview_configuration.interview_configuration.generate_round_numbers"
    },
	"Salary Structure Assignment": {
		"on_submit": "niyopolymers.hr.before_insert_salary_structure_assignment"
	},
	"Asset Maintenance Log": {
		"after_insert": "niyopolymers.assets.before_save_asset_maintenance_log",
		"on_submit": "niyopolymers.assets.create_stock_entry"
	},
	"Asset Repair": {
		"on_submit": "niyopolymers.assets.create_stock_entry_from_asset_repair"
	},
	"Leave Allocation": {
		"on_submit": "niyopolymers.hr.before_submit_leave_allocation"
	},
	"*": {
		"before_submit": "niyopolymers.accounts.before_submit_all_doctypes"
	},
	"Payment Entry": {
		"validate": "niyopolymers.accounts.before_insert_payment_entry",
		"before_submit": "niyopolymers.accounts.set_approver_name"
	},
	"Sales Invoice": {
		"validate": "niyopolymers.accounts.before_insert_sales_invoice",
		"before_submit": "niyopolymers.accounts.set_approver_name"
	},
	"Sales Order": {
		"before_submit": "niyopolymers.accounts.set_approver_name"
	},
	"Purchase Order": {
		"before_submit": "niyopolymers.accounts.set_approver_name"
	},	
	"Purchase Invoice": {
		"before_submit": "niyopolymers.accounts.set_approver_name"
	},
	"Material Request": {
		"before_submit": "niyopolymers.accounts.set_approver_name"
	},
	"Journal Entry": {
		"before_submit": "niyopolymers.accounts.set_approver_name"
	},
	"Payment Request and Authorization": {
		"before_submit": "niyopolymers.utils.set_approver_name"
	}

}

doctype_list_js = {
    "Salary Structure Assignment" : "public/js/salary_strucure_assignment_list.js",
	"Attendance": "public/js/attendance_list.js",
	"Leave Application" : "public/js/leave_application_list.js"
 	}

override_doctype_dashboards = {
	"Job Applicant": "niyopolymers.hr.override_job_applicant_dashboard",
}

scheduler_events = {
	"cron": {
		"59 11 * * 0": [
			"niyopolymers.hr.shift_rotate"
		],
		"59 * * * *": [
			"niyopolymers.hr.change_last_sync_of_checkin"
		],
		"0 0 * * *": [
			"niyopolymers.hr.trigger_mail_if_absent_consecutive_5_days"
		]
	},
	"hourly": [
        "niyopolymers.niyopolymers.employee_checkin.process_auto_attendance_for_holidays",
		"niyopolymers.hr.send_mail_to_employees_on_shift"
    ],
	"daily": [
        "niyopolymers.hr.maternity_leave_mail"
    ]
}

fixtures = [
	{
		"dt": "Custom Field",
		"filters": [
			[
				"dt",
				"in",
				["Asset Repair", "Asset Maintenance Task", "Asset Maintenance Log", "Delivery Note", "Employee", "Job Opening", "Employee Grade", "Salary Structure Assignment", "Employee Tax Exemption Proof Submission", "Supplier", "Customer", "Item", "Payment Entry", "Print Settings", "Purchase Invoice", "Purchase Order", "Sales Order", "Sales Invoice", "Material Request", "Purchase Receipt", "Journal Entry"]
			]
		]
	},
	{
		"dt": "Custom Script",
		"filters": [
			[
				"dt",
				"in",
				['Employee', 'Salary Structure', 'Salary Structure Assignment', 'Job Applicant', 'Job Opening', 'Payment Entry', 'Purchase Invoice', 'Asset Maintenance Log', 'Asset Repair', 'Quotation', 'Delivery Note', 'Item']
			]
		]
	},
	{
		'dt': 'Warning Letter Template',
		"filters": [
			[
				'name',
				'in', 
				['Consecutive Leave']
			]
		]
	},
	{
		"dt": "Workflow",
		"filters": [
			[
				"document_type",
				"in",
				["Journal Entry", "Sales Order", "Sales Invoice", "Payment Entry", "Purchase Order", "Purchase Invoice", "Material Request", "Payment Request and Authorization"]
			]
		]
	},
	{
		"dt": "Role",
		"filters": [
			[
				"name",
				"in",
				['Journal Entry Approver', 'Deputy PRA Approver', 'Accounts Viewer', 'Purchase Order Approver', 'PRA Approver', 'PRA Checker', 'CFO', 'Material Request Approver', 'Sales Invoice Approver', 'Sales Order Approver', 'Payment Entry Approver', 'Purchase Invoice Approver', 'CRV Approver', 'PCPV Approver', 'Chart of Accounts Manager', 'Document Deletor', 'Document canceller', 'Petty Cash Manager']
			]
		]
	}
]
