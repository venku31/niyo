import frappe
from frappe.utils import getdate, nowdate, cint, flt
import json
from datetime import date, timedelta, datetime
import time
from frappe.utils import formatdate
import ast
import itertools

@frappe.whitelist()
def set_approver_name(doc, method):
    doc.approver_person = doc.modified_by
    doc.approver_date = doc.modified

@frappe.whitelist()
def before_insert_payment_entry(doc, method):
    if doc.naming_series.startswith('CPV') and doc.mode_of_payment == 'Cheque':
        payment_entries = frappe.db.get_value('Payment Entry', {'reference_no': doc.reference_no, 'docstatus': ['!=', '2']}, ['name'])
        if payment_entries == None:
            return
        elif payment_entries != doc.name:    
            frappe.throw('Cheque/Reference no must be unique')   

def before_insert_sales_invoice(doc, method):
    naming_series = doc.naming_series.split('.')
    sales_invoice = frappe.db.get_value('Sales Invoice', {'fs_number': doc.fs_number, 'naming_series': ['like', '%'+naming_series[0]+'%'], 'docstatus': ['!=', '2']}, ['name'])
    if sales_invoice == None:
        return
    elif sales_invoice != doc.name:    
        frappe.throw('FS Numer must be unique')   
