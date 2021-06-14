from erpnext.hr.doctype.attendance_request.attendance_request import AttendanceRequest
from frappe.utils import date_diff, add_days, getdate
import frappe

def create_attendance(self):
    print('Custom Attendance request file')
    request_days = date_diff(self.to_date, self.from_date) + 1
    for number in range(request_days):
        attendance_date = add_days(self.from_date, number)
        skip_attendance = self.validate_if_attendance_not_applicable(attendance_date)
        if not skip_attendance:
            attendance = frappe.new_doc("Attendance")
            attendance.employee = self.employee
            attendance.employee_name = self.employee_name
            if self.half_day and date_diff(getdate(self.half_day_date), getdate(attendance_date)) == 0:
                attendance.status = "Half Day"
            else:
                attendance.status = "Present"
            attendance.attendance_date = attendance_date
            attendance.company = self.company
            attendance.shift = self.shift
            attendance.working_hours = self.working_hours
            attendance.attendance_request = self.name
            attendance.save(ignore_permissions=True)
            attendance.submit()


AttendanceRequest.create_attendance = create_attendance