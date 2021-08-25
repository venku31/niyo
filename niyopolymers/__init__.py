# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '1.0.3'

from niyopolymers.overrides.attendance_request import AttendanceRequest

def delivery_autoname(doc,method):
    doc.name = 'DN-{0}-{1}'.format(frappe.utils.now_datetime().year,doc.delivery_slip_number)
