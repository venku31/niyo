import frappe
from frappe.utils import getdate, nowdate, cint, flt
import json
from datetime import date, timedelta, datetime
import time
from frappe.utils import formatdate
import ast
import itertools
from erpnext.hr.doctype.employee_checkin.employee_checkin import mark_attendance_and_link_log
from frappe.utils.background_jobs import enqueue

@frappe.whitelist()
def set_approver_name(doc, method):
	doc.approver_person = doc.modified_by
	doc.approver_date = doc.modified

	get_approver_name = frappe.db.get_value('Comment', {'reference_name':doc.name, 'content': 'Sent for Approval'}, 'owner')
	print(get_approver_name)
	get_approved_date = frappe.db.get_value('Comment', {'reference_name':doc.name, 'content': 'Sent for Approval'}, 'modified')
	print(get_approved_date)
	frappe.db.set_value(doc.doctype, {'name': doc.name}, 'checked_person', get_approver_name)
	frappe.db.set_value(doc.doctype, {'name': doc.name}, 'checked_date', get_approved_date)

def trigger_mail_of_pending_todo():
	pending_todos = frappe.db.get_all('ToDo', filters={'status': 'Open'}, fields=['name', 'description'])
	print(pending_todos[0]['name'])
	if pending_todos:
		notification = frappe.get_doc('Notification', 'Pending ToDo')
		doc = frappe.get_doc('ToDo', pending_todos[0]['name'])
		doc.todos = pending_todos
		args={'doc': doc}
		recipients, cc, bcc = notification.get_list_of_recipients(doc, args)
		print(cc)
		frappe.enqueue(method=frappe.sendmail, recipients=recipients, cc = cc, bcc = bcc, sender=None, 
		subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))

