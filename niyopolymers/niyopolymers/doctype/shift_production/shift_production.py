# -*- coding: utf-8 -*-
# Copyright (c) 2021, Atriina and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ShiftProduction(Document):
	pass

@frappe.whitelist()
def create_stock_entry(doc, handler=""):
    se = frappe.new_doc("Stock Entry")
    se.update({ "purpose": "Manufacture" , "stock_entry_type": "Manufacture"})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.preform, "qty": se_item.blowing, "s_warehouse": "Stores - NP"})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.product_code, "qty": se_item.blowing_perform, "t_warehouse":"Finished Goods - NP"})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.rejection_item, "qty": se_item.rejection, "t_warehouse": "Scrap Warehouse - NP"})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.rejection_white, "qty": se_item.white, "t_warehouse": "Scrap Warehouse - NP"})
    for se_item in doc.items:
        se.append("items", { "item_code":se_item.rejection_hot, "qty": se_item.hot, "t_warehouse": "Scrap Warehouse - NP"})

#    frappe.msgprint('Stock Entry is created please submit the stock entry')
        se.docstatus=1
        se.insert()
