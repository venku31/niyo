# -*- coding: utf-8 -*-
# Copyright (c) 2021, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ShiftProduction(Document):
	pass

# @frappe.whitelist()
def create_stock_entry(doc, handler=""):
    se = frappe.new_doc("Stock Entry")
    se.update({ "purpose": "Manufacture" , "stock_entry_type": "Manufacture"})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.preform, "qty": se_item.blowing, "s_warehouse": se_item.rm_warehouse,"transfer_qty" : se_item.blowing,"conversion_factor": 1,"uom" : se_item.uom})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.product_code, "qty": se_item.blowing_perform, "t_warehouse":se_item.fg_warehouse,"transfer_qty" : se_item.blowing_perform,"conversion_factor": 1,"uom" : se_item.uom})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.rejection_item, "qty": se_item.rejection, "t_warehouse": se_item.rejection_warehouse,"transfer_qty" : se_item.rejection,"conversion_factor": 1,"uom" : se_item.uom})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.rejection_white, "qty": se_item.white, "t_warehouse": se_item.rejection_warehouse,"transfer_qty" : se_item.rejection_white,"conversion_factor": 1,"uom" : se_item.uom})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.rejection_hot, "qty": se_item.hot, "t_warehouse": se_item.rejection_warehouse,"transfer_qty" : se_item.rejection_hot,"conversion_factor": 1,"uom" : se_item.uom})

#    frappe.msgprint('Stock Entry is created please submit the stock entry')
    se.docstatus=1
    se.insert()
