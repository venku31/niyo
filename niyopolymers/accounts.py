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

def auto_set_fs_number(doc, method):
    if not doc.amended_from:
        selling_settings = frappe.get_single('Selling Settings')
        if selling_settings.last_fs_number:
            sales_invoice = frappe.db.get_all('Sales Invoice', filters={}, fields=['fs_number'], order_by ='fs_number desc')
            if not sales_invoice:
                doc.fs_number = "{0:08d}".format(int(selling_settings.last_fs_number)+1)
            else:    
                doc.fs_number = "{0:08d}".format(int(sales_invoice[0]['fs_number'])+1)            