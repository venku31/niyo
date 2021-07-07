import frappe

def execute():
    hr_settings = frappe.get_single("HR Settings")

    hr_settings.update(
        {
            'auto_leave_encashment': 0,
            'check_vacancies': 0,
            'disable_rounded_total': 1,
            'email_salary_slip_to_employee': 1,
            'emp_created_by': 'Naming Series',
            'encrypt_salary_slips_in_emails': 0,
            'expense_approver_mandatory_in_expense_claim': 1,
            'include_holidays_in_total_working_days': 0,
            'leave_approval_notification_template': 'Leave Approval Notification',
            'leave_approver_mandatory_in_leave_application': 0,
            'leave_status_notification_template': 'Leave Status Notification',
            'max_working_hours_against_timesheet': 0,
            'show_leaves_of_all_department_members_in_calendar': 0,
            'stop_birthday_reminders': 0
        }
    )
    hr_settings.save()
    frappe.db.commit()