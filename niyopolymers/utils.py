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

def send_sales_and_purchase_details():
	today_sales_invoice = frappe.db.sql("""
		select coalesce(coalesce(sum(grand_total), 0), 0) from `tabSales Invoice`
		where posting_date = '{}'
	""".format(frappe.utils.nowdate()))
	yearly_sales_invoice = frappe.db.sql("""
		select coalesce(sum(grand_total), 0) from `tabSales Invoice`
		where year(posting_date)=year(curdate())
	""")
	today_purchase_invoice = frappe.db.sql("""
		select coalesce(sum(grand_total), 0) from `tabPurchase Invoice`
		where posting_date = '{}'
	""".format(frappe.utils.nowdate()))
	yearly_purchase_invoice = frappe.db.sql("""
		select coalesce(sum(grand_total), 0) from `tabPurchase Invoice`
		where year(posting_date)=year(curdate())
	""")
	pay_payment_entry = frappe.db.sql("""
		select coalesce(sum(paid_amount), 0) from `tabPayment Entry`
		where posting_date = '{}' and payment_type = 'Pay'
	""".format(frappe.utils.nowdate()))
	receive_payment_entry = frappe.db.sql("""
		select coalesce(sum(paid_amount), 0) from `tabPayment Entry`
		where posting_date = '{}' and payment_type = 'Receive'
	""")

	notification = frappe.get_doc('Notification', 'Sales and Purchase Report')
	get_sales_invoice = frappe.db.sql("""
		select name from `tabSales Invoice`
		where posting_date = '{}' limit 1
	""".format(frappe.utils.nowdate()))
	if get_sales_invoice:
		doc = frappe.get_doc('Sales Invoice', get_sales_invoice[0][0])
		args={'doc': doc}
		doc.today_sales_invoice = today_sales_invoice[0][0]
		doc.yearly_sales_invoice = yearly_sales_invoice[0][0]
		doc.pay_payment_entry = pay_payment_entry[0][0]
		doc.receive_payment_entry = receive_payment_entry[0][0]
		doc.today_purchase_invoice = today_purchase_invoice[0][0]
		doc.yearly_purchase_invoice = yearly_purchase_invoice[0][0]

		recipients, cc, bcc = notification.get_list_of_recipients(doc, args)
		frappe.enqueue(method=frappe.sendmail, recipients=recipients, cc = cc, bcc = bcc, sender=None, 
		subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))
