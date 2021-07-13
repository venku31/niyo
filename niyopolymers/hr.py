import frappe
from frappe.utils import getdate, nowdate, cint, flt
import json
from datetime import date, timedelta, datetime
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words
import time
from frappe.utils import formatdate
import ast
import itertools
from erpnext.hr.doctype.employee_checkin.employee_checkin import mark_attendance_and_link_log
from frappe.utils.background_jobs import enqueue
from erpnext.hr.doctype.leave_application.leave_application import get_leave_details

def override_job_applicant_dashboard(data):
    print(data)
    return {
        'fieldname': 'job_applicant',
        'transactions': [
            # {
            #     'items': ['Employee', 'Employee Onboarding']
            # },
            # {
            #     'items': ['Job Offer']
            # },
            # {
            #     'items': ['Interview']
            # },
        ],
    }

@frappe.whitelist()
def before_submit_leave_allocation(doc, method):
    def calculate_years_of_experience(doj, till_date=None):
        from dateutil.relativedelta import relativedelta
        if not till_date:
            from datetime import datetime 
            till_date = datetime.today()

        try: 
            experience = relativedelta(till_date, doj).years
        except AttributeError:
            experience = 0
        
        return experience

    doj = frappe.db.get_value('Employee', doc.employee, 'date_of_joining')
    leave_date = frappe.db.get_value('Leave Allocation', doc.name, 'from_date')
    total_experience = calculate_years_of_experience(doj, leave_date)
    leave_policy = frappe.get_doc('Leave Policy', doc.leave_policy)
    base_leave_count = leave_policy.leave_policy_details[0].annual_allocation
    get_total_leaves = base_leave_count+total_experience
    doc.new_leaves_allocated = get_total_leaves
    doc.set_total_leaves_allocated()

@frappe.whitelist()
def set_conversion_rate(employee):
    if employee:
        employee_list = frappe.db.get_all('Payroll Employee Detail', {'employee': employee}, ['parent'], order_by='creation desc', limit=1, as_list=1)
        if employee_list:
            get_conversion_rate = frappe.db.get_value('Payroll Entry', employee_list[0][0], 'conversion_rate')
            return get_conversion_rate

@frappe.whitelist()
def before_save_salary_slip(doc, method):
    doc.normal_ot_hours = 0
    doc.sunday_ot_hours = 0
    doc.holiday_ot_hours_ = 0
    doc.night_ot_hours = 0
    doc.total_working_days = 0
    doc.total_night_shift_days = 0
    doc.paid_leaves = 0

    overtime_applicable = frappe.db.get_value('Employee', doc.employee, 'is_overtime_applicable')
    if overtime_applicable:
        daily_overtime(doc)
        night_overtime(doc)
        sunday_overtime(doc)
        holiday_overtime(doc)

    before_save(doc, method)
    
def before_insert_salary_slip(doc, method):
    doc.normal_ot_hours = 0
    doc.sunday_ot_hours = 0
    doc.holiday_ot_hours_ = 0
    doc.night_ot_hours = 0
    doc.total_working_days = 0
    doc.total_night_shift_days = 0
    doc.paid_leaves = 0

    absent_attendances = frappe.get_list('Attendance', [
        ['employee', '=', doc.employee],
        ['attendance_date', 'between', [doc.start_date, doc.end_date]],
        ['status', 'in', ['Absent', 'Half Day']],
        ['docstatus', '=', 1],
        ['leave_application', 'is', 'not set']
    ])

    for i in absent_attendances:
        process_lop_leave_for_attendance(i.name)

    doc.get_leave_details()

    overtime_applicable = frappe.db.get_value('Employee', doc.employee, 'is_overtime_applicable')
    if overtime_applicable:
        daily_overtime(doc)
        night_overtime(doc)
        sunday_overtime(doc)
        holiday_overtime(doc)

    if doc.payroll_entry:  
        payroll_entry = frappe.db.get_value('Payroll Entry', doc.payroll_entry, 'monthly_attendance_bonus')
        if payroll_entry:
            doc.attendance_bonus = payroll_entry
        shift_allowance = frappe.db.get_value('Payroll Entry', doc.payroll_entry, 'allowance_per_night_shift')    
        if shift_allowance:
            doc.allowance_per_night_shift = shift_allowance        

def before_save(doc, method):
    company = frappe.defaults.get_user_default("company") 
    default_holiday = frappe.db.get_value('Company', company, 'default_holiday_list')
    holiday_ = []
    if default_holiday:
        holiday_day = frappe.db.get_value('Holiday List', {'name': default_holiday}, 'weekly_off')
        holiday = frappe.db.get_all('Holiday', filters={'parent': default_holiday, 'description': holiday_day, 'holiday_date': ('between',[ doc.start_date, doc.end_date])},  fields=['holiday_date'], as_list=1)

        for i in holiday:
            splitdate = i[0].strftime('%Y-%m-%d')
            holiday_.append(splitdate)
            
        total = date_diff(doc.end_date, doc.start_date) + 1   
        hr_settings = frappe.db.get_single_value('HR Settings', 'include_holidays_in_total_working_days')
        if hr_settings == 0: 
            doc.total_working_days = total - len(holiday_)
            doc.payment_days = doc.total_working_days - doc.leave_without_pay
        else:
            doc.total_working_days = total
            doc.payment_days = doc.total_working_days - doc.leave_without_pay

        paid_leaves = frappe.db.get_all('Leave Application', filters={'leave_type': ['!=', 'Leave Without Pay'], 'docstatus': ['=', 1]}, fields=['count(name) as total'])
        if paid_leaves:
            doc.paid_leaves = paid_leaves[0]['total']
        doc.calculate_component_amounts("earnings")
        doc.calculate_component_amounts("deductions")


def process_lop_leave_for_attendance(attendance_name):
    attendance = frappe.get_doc('Attendance', attendance_name)

    pending_leave_applications = frappe.get_list('Leave Application', [
        ['employee', '=', attendance.employee],
        ['docstatus', '=', 0],
        ['status', '=', 'Open'],
        ['from_date', '<=', attendance.attendance_date],
        ['to_date', '>=', attendance.attendance_date]
    ])

    for i in pending_leave_applications:
        leave_application = frappe.get_doc('Leave Application', i.name)
        leave_application.docstatus = 0
        leave_application.status = 'Rejected'
        leave_application.workflow_state = 'Rejected'
        leave_application.save()

    leave_application = frappe.new_doc('Leave Application')
    leave_application.employee = attendance.employee
    leave_application.company = attendance.company
    leave_application.from_date = attendance.attendance_date.strftime('%Y-%m-%d')
    leave_application.to_date = attendance.attendance_date.strftime('%Y-%m-%d')
    leave_application.half_day = 1 if attendance.status == 'Half Day' else 0
    leave_application.leave_type = 'Leave Without Pay'
    leave_application.insert()

    leave_application.reload()
    leave_application.docstatus = 1
    leave_application.status = 'Approved'
    leave_application.workflow_state = 'Approved'
    leave_application.save()

    frappe.db.commit()
    # process_auto_attendance_for_holidays(doc)

@frappe.whitelist()
def on_update_employee(doc, method):
    get_salary_structure_ass = frappe.get_all('Salary Structure Assignment', filters={'employee': doc.employee, 'docstatus': 1})
    if get_salary_structure_ass:
        # grade = frappe.db.get_value('Employee Grade', doc.grade, 'default_salary_structure')
        # frappe.db.set_value('Salary Structure Assignment', {'name': get_salary_structure_ass[0].name}, 'salary_structure', grade)
        employee_grade = frappe.db.get_value('Employee Grade', doc.grade, 'base_amount')
        if employee_grade:
            frappe.db.set_value('Salary Structure Assignment', {'name': get_salary_structure_ass[0].name}, 'grade', doc.grade)
            frappe.db.set_value('Salary Structure Assignment', {'name': get_salary_structure_ass[0].name}, 'base', employee_grade)
            frappe.db.set_value('Salary Structure Assignment', {'name': get_salary_structure_ass[0].name}, 'salary_in_usd', employee_grade)
            frappe.db.set_value('Salary Structure Assignment', {'name': get_salary_structure_ass[0].name}, 'promotion', 'Salary Updated')
            frappe.db.commit()

def daily_overtime(doc):
    employee_holiday = frappe.db.get_value('Employee', doc.employee, 'holiday_list')
    if employee_holiday:
        holiday = frappe.db.get_all('Holiday', filters={'parent': employee_holiday, 'holiday_date': ('between',[ doc.start_date, doc.end_date])},  fields=['holiday_date'], as_list=1)
        
        holiday_ = []
        for i in holiday:
            splitdate = i[0].strftime('%Y-%m-%d')
            holiday_.append(splitdate)
        shift = frappe.db.get_value('Employee', {'employee': doc.employee}, ['default_shift'])
        if shift: 

            filters = [
                ['employee', '=', doc.employee],
                ['attendance_date', '<=', doc.end_date],
                ['attendance_date', '>=', doc.start_date],
                ['attendance_date', 'not in', holiday_],
                ['docstatus', '!=', 2],
                ['status', '=', 'Present'],
                ['shift', '!=', 'Night Shift']
            ]

            attendances = frappe.db.get_all('Attendance', filters=filters, fields=['working_hours', 'shift'], as_list=True)
            for i in attendances:
                shift_start = frappe.db.get_value('Shift Type',i[1],'start_time')
                shift_end = frappe.db.get_value('Shift Type',i[1],'end_time')
                if shift_end is not None and shift_start is not None:
                    shift_time = shift_end - shift_start
                    hours = shift_time.seconds
                    total = hours/3600
                    
                    if (i[0] > total):
                        # doc.total_day_shift_days += 1
                        doc.normal_ot_hours += (i[0] - total)
                    
def night_overtime(doc):
    holiday = frappe.db.get_all('Holiday', filters={'holiday_date': ('between',[ doc.start_date, doc.end_date])},  fields=['holiday_date'], as_list=1)
   
    holiday_ = []
    for i in holiday:
        splitdate = i[0].strftime('%Y-%m-%d')
        holiday_.append(splitdate)
    # shift = frappe.db.get_value('Employee', {'employee': doc.employee, 'is_overtime_applicable': 1}, ['default_shift'])
    # if shift: 

    filters = [
        ['employee', '=', doc.employee],
        ['attendance_date', '<=', doc.end_date],
        ['attendance_date', '>=', doc.start_date],
        ['attendance_date', 'not in', holiday_],
        ['docstatus', '!=', 2],
        ['status', '=', 'Present'],
        ['shift', '=', 'Night Shift']
    ]

    attendances = frappe.db.get_all('Attendance', filters=filters, fields=['working_hours'], as_list=True)
    attendance_list = []
    for i in attendances:
        for j in i:
            attendance_list.append(j)

    shift_start = frappe.db.get_value('Shift Type','Night Shift','start_time')
    shift_end = frappe.db.get_value('Shift Type','Night Shift','end_time')
    shift_time = shift_end - shift_start
    hours = shift_time.seconds//3600
    for i in attendance_list:
        # i = int(i)
        if i > hours:
            doc.total_night_shift_days += 1
            doc.night_ot_hours +=  (i - hours)
    
def sunday_overtime(doc):
    employee_holiday = frappe.db.get_value('Employee', doc.employee, 'holiday_list')
    if employee_holiday:
        holiday_day = frappe.db.get_value('Holiday List', {'name': employee_holiday}, 'weekly_off')
        holiday = frappe.db.get_all('Holiday', filters={'parent': employee_holiday, 'description': holiday_day, 'holiday_date': ('between',[ doc.start_date, doc.end_date])},  fields=['holiday_date'], as_list=1)
    
        holiday_ = []
        for i in holiday:
            splitdate = i[0].strftime('%Y-%m-%d')
            holiday_.append(splitdate)

        filters = [
            ['employee', '=', doc.employee],
            ['attendance_date', 'in', holiday_],
            ['docstatus', '!=', 2],
            ['status', '=', 'Present']
        ]
        
        attendances = frappe.db.get_all('Attendance', filters=filters, fields=['working_hours'], as_list=True)
        
        # if attendances:
        #     doc.total_working_sunday = len(attendances)

        for i in attendances:    
            doc.sunday_ot_hours += i[0]
       
def holiday_overtime(doc):
    employee_holiday = frappe.db.get_value('Employee', doc.employee, 'holiday_list')
    if employee_holiday:
        holiday_day = frappe.db.get_value('Holiday List', {'name': employee_holiday}, 'weekly_off')
        holiday = frappe.db.get_all('Holiday', filters={'parent': employee_holiday, 'description': holiday_day, 'holiday_date': ('between',[ doc.start_date, doc.end_date])},  fields=['holiday_date'], as_list=1)
    
        holiday_ = []
        for i in holiday:
            splitsundaydate = i[0].strftime('%Y-%m-%d')
            holiday_.append(splitsundaydate)
        
        filters = [
            ['employee', '=', doc.employee],
            ['attendance_date', 'in', holiday_],
            ['docstatus', '!=', 2],
            ['status', '=', 'Present']
        ]
        
        attendances = frappe.db.get_all('Attendance', filters=filters, fields=['working_hours'], as_list=True)

        for i in attendances:
            doc.holiday_ot_hours_ += i[0]

@frappe.whitelist(allow_guest=True)
def trigger_mail_if_absent_consecutive_5_days():

    attendance = frappe.db.sql("""
    select count(attendance_date) as count, employee, employee_name, name
    from `tabAttendance` 
    where  attendance_date >= DATE_SUB(CURDATE(), INTERVAL 5 DAY) 
    and status in ('Absent', 'On Leave') and docstatus = 1 group by employee order by attendance_date ;

    """, as_dict = 1)
    print(attendance)
    if attendance:
        employee = []
        for i in attendance:
            if i['count'] >= 5:
                employee.append({'employee': i['employee_name']})
                get_employee_warnings = frappe.get_all('Warning Letter Detail', filters={'parent': i['employee']}, fields=['warning_number'], order_by='warning_number desc', page_length=1)
                warning_template = frappe.db.get_value('Warning Letter Template', 'Consecutive Leave', 'name')
                warning_letter = frappe.new_doc('Warning Letter')
                warning_letter.employee = i['employee']
                warning_letter.template = warning_template

                if not get_employee_warnings:
                    # frappe.throw('ja na be')
                    warning_letter.warning_number = 1
                
                else:
                    warning_letter.warning_number = get_employee_warnings[0]['warning_number'] + 1
                
                warning_letter.save(ignore_permissions=True)

                set_employee_warnings = frappe.get_doc('Employee', i['employee'])
                set_employee_warnings.append('warnings', {
                    'warning_letter': warning_letter.name
                })
                if not get_employee_warnings:
                    set_employee_warnings.warnings_letters_given = 1
                else:
                    set_employee_warnings.warnings_letters_given = get_employee_warnings[0]['warning_number']+1
                set_employee_warnings.save(ignore_permissions=True)
        
        if len(employee) >= 1:
            notification = frappe.get_doc('Notification', 'Consecutive Leave')
            doc = frappe.get_doc('Attendance', attendance[0]['name'])
            doc.employees = employee
            args={'doc': doc}
            recipients, cc, bcc = notification.get_list_of_recipients(doc, args)
            frappe.enqueue(method=frappe.sendmail, recipients=cc, sender=None, now=True,
                    subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))
        
@frappe.whitelist()
def update_salary_structure_assignment_rate(doc, method):
    employee_list = frappe.db.get_all('Payroll Employee Detail', {'parent': doc.name}, ['employee'], as_list=1)
    if employee_list:
        for i in employee_list:
            get_base_amount = frappe.db.get_value('Salary Structure Assignment', {'employee': i[0], 'docstatus': ['!=', 2]}, 'base')
            if get_base_amount:
                frappe.db.set_value('Salary Structure Assignment', {'employee': i[0], 'docstatus': ['!=', 2]}, 'salary_in_birr', int(get_base_amount) * int(doc.conversion_rate))
                frappe.db.commit()

def shift_rotate():
    employee = frappe.db.get_all('Employee', filters = {'default_shift': ['is', 'set'], 'shift_rotate': 1}, fields=['name'], as_list=1)
    if employee:
        employee_store_in_list = [i[0] for i in employee]
        employee_convert_tuple = tuple(employee_store_in_list)
        shifts = frappe.db.get_all('Shift Type', filters={'name': ['in', ['Day Shift', 'Night Shift']]}, fields=['name'], as_list=1)
        if shifts:
            shift_store_in_list = [i[0] for i in shifts]
            shift_convert_tuple = tuple(shift_store_in_list)
            frappe.db.sql("""
                            Update `tabEmployee` 
                            SET default_shift = CASE 
                            WHEN default_shift='{0}' THEN '{1}' 
                            WHEN default_shift='{1}' THEN '{0}' 
                            ELSE default_shift END where employee in {2}
                            """.format(shift_convert_tuple[0], shift_convert_tuple[1], employee_convert_tuple))
            frappe.db.commit()

def get_employees(doc, **kwargs):
		conditions, values = [], []
		for field, value in kwargs.items():
			if value:
				conditions.append("{0}=%s".format(field))
				values.append(value)

		condition_str = " and " + " and ".join(conditions) if conditions else ""

		employees = frappe.db.sql_list("select name from tabEmployee where status='Active' {condition}"
			.format(condition=condition_str), tuple(values))

		return employees

@frappe.whitelist()
def before_insert_salary_structure_assignment(doc, method):
    # get_employee_base_amount = frappe.db.get_value('Employee Grade', {'default_salary_structure': doc.salary_structure}, 'base_amount')
    # if get_employee_base_amount:
    #     frappe.db.set_value('Salary Structure Assignment', {'name': doc.name}, 'base', get_employee_base_amount)
    #     frappe.db.commit()   
    frappe.db.set_value('Salary Structure Assignment', {'name': doc.name}, 'salary_in_usd', doc.base)

@frappe.whitelist()
def assign_salary_structure(doc, company=None, grade=None, department=None, designation=None,employee=None,
        from_date=None, base=None, variable=None, income_tax_slab=None):
    employees = get_employees(doc, company= company, grade= grade,department= department,designation= designation,name=employee)

    if employees:
        if len(employees) > 20:
            frappe.enqueue(assign_salary_structure_for_employees, timeout=600,
                employees=employees, salary_structure=doc,from_date=from_date,
                base=base, variable=variable, income_tax_slab=income_tax_slab)
        else:
            assign_salary_structure_for_employees(employees, doc, from_date=from_date,
                base=base, variable=variable, income_tax_slab=income_tax_slab)
    else:
        frappe.msgprint(frappe._("No Employee Found"))

def assign_salary_structure_for_employees(employees, salary_structure, from_date=None, base=None, variable=None, income_tax_slab=None):
	salary_structures_assignments = []
	existing_assignments_for = get_existing_assignments(employees, salary_structure, from_date)
	count=0
	for employee in employees:
		if employee in existing_assignments_for:
			continue
		count +=1

		salary_structures_assignment = create_salary_structures_assignment(employee,
			salary_structure, from_date, base, variable, income_tax_slab)
		salary_structures_assignments.append(salary_structures_assignment)
		frappe.publish_progress(count*100/len(set(employees) - set(existing_assignments_for)), title = frappe._("Assigning Structures..."))

	if salary_structures_assignments:
		frappe.msgprint(frappe._("Structures have been assigned successfully"))


def create_salary_structures_assignment(employee, salary_structure, from_date, base, variable, income_tax_slab=None):
    salary_structure = ast.literal_eval(salary_structure)
    assignment = frappe.new_doc("Salary Structure Assignment")
    assignment.employee = employee
    assignment.salary_structure = salary_structure['name']
    assignment.company = salary_structure['company']
    assignment.from_date = from_date
    assignment.base = base
    assignment.variable = variable
    assignment.income_tax_slab = income_tax_slab
    assignment.save(ignore_permissions = True)
    assignment.submit()
    return assignment.name

def get_existing_assignments(employees, salary_structure, from_date):
    salary_structure = ast.literal_eval(salary_structure)
    salary_structures_assignments = frappe.db.sql_list("""
        select distinct employee from `tabSalary Structure Assignment`
        where salary_structure=%s and employee in (%s)
        and company= %s and docstatus=1
    """ % ('%s', ', '.join(['%s']*len(employees)),'%s'), [salary_structure['name']] + employees+[salary_structure['company']])
    if salary_structures_assignments:
        frappe.msgprint(frappe._("Skipping Salary Structure Assignment for the following employees, as Salary Structure Assignment records already exists against them. {0}")
            .format("\n".join(salary_structures_assignments)))
    return salary_structures_assignments

@frappe.whitelist()
def existing_interview_rounds(job_applicant, job_opening):
    interview = frappe.get_list('Interview', filters={'job_applicant': job_applicant}, as_list = 1)
    if len(interview) > 0:
        rounds = frappe.get_list('Interview Round', filters={'interview': interview[0][0]}, order_by='round_number')
        print(len(rounds))
        if len(rounds) > 0:
            return True
        else:
            return False

@frappe.whitelist()
def get_interview_rounds(job_applicant, job_opening):
    interview = frappe.get_all('Interview', filters={'job_applicant': job_applicant, }, as_list = 1)
    rounds = frappe.get_all('Interview Round', filters={'interview': interview[0][0]}, fields=['*'], order_by='round_number')
    print(rounds)
    list2 = []
    for i in rounds:
        comment = []
        if i['_comments'] is not None:
            a = json.loads(i['_comments'])
            for j in a:
                comment.append(j['comment'])
            
        print(comment)
       
        interviewer = frappe.get_all('Interviewer', filters={'parent': i['name']}, fields=['employee', 'employee_name'] )
        l_ = []
        for row in interviewer:
                l_.append("{}-{}".format(row['employee'], row['employee_name']))    
        k =  [
                # {
                #     'label': i['round_number'],
                #     'fieldname': '',
                #     'fieldtype': 'Section Break'
                # },
                {
                    'label': 'Round Number',
                    'fieldname': 'round_number',
                    'fieldtype': 'Data',
                    'default': i['round_number'],
                    'read_only': 1
                },
                {
                    'label': 'Date',
                    'fieldname': 'date',
                    'fieldtype': 'Datetime',
                    'read_only': 1,
                    'default': i['date']
                },
                {
                    'label': '',
                    'fieldname': '',
                    'fieldtype': 'Column Break'
                },
                {
                    'label': 'Round Name',
                    'fieldname': 'round_name',
                    'fieldtype': 'Data',
                    'default': i['round'],
                    'read_only': 1
                },
                {
                    'label': 'Status',
                    'fieldname': 'status',
                    'fieldtype': 'Data',
                    'default': i['status'],
                    'read_only': 1
                },
                {
                    'label': '',
                    'fieldname': '',
                    'fieldtype': 'Column Break'
                },
                {
                    "label": "Interviewer's",
                    'fieldname': "interviewers",
                    "fieldtype": "Small Text",
                    "options": "Interviewer",
                    '_link_field':'employee',
                    'default': '\n'.join(l_),
                    'read_only': 1
                },
                {
                    "label": "Overall Recommendation",
                    'fieldname': "overall_recommendation",
                    "fieldtype": "Data",
                    'read_only': 1,
                    'default': i['overall_recommendation']
                },
                {
                    'label': '',
                    'fieldname': '',
                    'fieldtype': 'Section Break'

                }
            ]  
        list2.append(k)
        
        rounds_feedback = frappe.get_all('Interview Round Feedback', filters={'parent': i['name']}, fields=['*'])
        print(rounds_feedback, 'rounds feedback')
        if len(rounds_feedback) > 0:
            for i in rounds_feedback:
                l = [
                    {
                        'label': 'Skill',
                        'fieldname': 'skill',
                        'fieldtype': 'Link',
                        'read_only': 1,
                        'default': i['skill']
                    },
                    {
                        'label': '',
                        'fieldname': '',
                        'fieldtype': 'Column Break'
                    },
                    {
                        'label': 'Remark',
                        'fieldname': 'remark',
                        'fieldtype': 'Small Text',
                        'read_only': 1,
                        'default': i['remark']
                    },
                    {
                        'label': '',
                        'fieldname': '',
                        'fieldtype': 'Column Break'
                    },
                    {
                        'label': 'Rating',
                        'fieldname': 'rating',
                        'fieldtype': 'Int',
                        'read_only': 1,
                        'default': i['rating1']
                    },
                     
                    {
                        'label': '',
                        'fieldname': '',
                        'fieldtype': 'Section Break'
                    }

                ]
                list2.append(l)
        c = [
                {
                    'label': 'Comment',
                    'fieldname': 'comment',
                    'fieldtype': 'HTML Editor',
                    'read_only': 1,
                    'default': comment,
                    'Bold': 1
                    # 'default': a[0]['comment']
                },
                {
                    'label': '',
                    'fieldname': '',
                    'fieldtype': 'Section Break'
                }
            ]    
        list2.append(c)   
    interview_rounds = [val for sublist in list2 for val in sublist] 
    interviewer = frappe.get_doc('DocType', 'Interviewer')
    return {'interview_rounds': interview_rounds, 'interviewer': interviewer}

@frappe.whitelist()
def get_interview_and_interview_rounds(job_applicant, job_opening):
    interview = frappe.get_list("Interview", filters={'job_applicant': job_applicant}, fields=['*'])
    designation = frappe.get_list("Job Opening", filters={'name': job_opening}, fields=['designation'], as_list=1)
    print(designation)
    configuration = frappe.get_all('Interview Configuration', filters={'designation': designation[0][0]})
    print(len(configuration))
    if len(configuration) == 0:
        return False
    if len(interview) == 0:
        print("In if condition")
        rounds =  [
            {
                'label': 'Round 1',
                'fieldname': '',
                'fieldtype': 'Section Break'
            },

            {
                'label': 'Date',
                'fieldname': 'date',
                'fieldtype': 'Datetime'
            },
            {
                'label': '',
                'fieldname': '',
                'fieldtype': 'Column Break'
            },
            {
                    "label": "Interviewers",
                    'fieldname': "interviewers",
                    "fieldtype": "Table MultiSelect",
                    "options": "Interviewer",
                    '_link_field':'employee'
            }
        ] 
        interviewer = frappe.get_doc('DocType', 'Interviewer')
        return {'rounds':rounds, 'interviewer': interviewer}  
    else:
        print("in else condition")
        # created interview section
        list1 = []
        k = [
                {
                    'label': 'Interview',
                    'fieldname': 'interview',
                    'fieldtype': 'Link',
                    'options': 'Interview',
                    'default': interview[0]['name'],
                    'read_only': 1
                },
                {
                    'label': 'Job Opening',
                    'fieldname': 'job_opening',
                    'fieldtype': 'Link',
                    'options': 'Job Opening',
                    'default': interview[0]['job_opening'],
                    'read_only': 1
                },
                {
                    'label': '',
                    'fieldname': '',
                    'fieldtype': 'Column Break'
                },
                {
                    'label': 'Job Applicant',
                    'fieldname': 'job_applicant',
                    'fieldtype': 'Link',
                    'options': 'Job Applicant',
                    'default': interview[0]['job_applicant_name'],
                    'read_only': 1
                },
                {
                    'label': 'Designation',
                    'fieldname': 'designation',
                    'fieldtype': 'Link',
                    'options': 'Designation',
                    'default': interview[0]['designation'],
                    'read_only': 1
                }
        ]
        list1.append(k)
        interview_round = frappe.get_list('Interview Round', filters={'interview': interview[0]['name']}, fields=['*'], order_by = 'round_number')
        print(interview_round)
        for l in interview_round:
            
            interviewer = frappe.get_all('Interviewer', filters={'parent': l['name']}, fields=['employee', 'employee_name'] )
            l_ = []
            for row in interviewer:
                l_.append("{}-{}".format(row['employee'], row['employee_name']))
            #   created rounds section
            m =  [
                {
                    'label': 'Round' + ' ' + str(l['round_number']) + '-' + l['round'],
                    'fieldname': '',
                    'fieldtype': 'Section Break'
                },
                {
                    'label': 'Date',
                    'fieldname': 'date_',
                    'fieldtype': 'Datetime',
                    'default': l['date'],
                    'read_only': 1

                },
                {
                    'label': '',
                    'fieldname': '',
                    'fieldtype': 'Column Break'
                },
                {
                    "label": "Interviewers",
                    'fieldname': "interviewers",
                    "fieldtype": "Small Text",
                    "options": "Interviewer",
                    '_link_field':'employee',
                    'default': '\n'.join(l_),
                    'read_only': 1
                }
                
                ]
            list1.append(m)
        existing_rounds_ = frappe.get_list("Interview Round", fields=["round"], filters={
                                'interview': interview[0]['name']}, as_list=1)
        existing_rounds = [i[0] for i in existing_rounds_]
        # print(designation[0][0])
        rounds = frappe.get_list("Interview Round Configuration", fields=['*'], filters={'parent': interview[0]['designation'], 'round_name': ['not in', existing_rounds]}, order_by='round_number')
        if len(rounds) > 0:
            # new rounds section
            y =  [
                {
                    'label': 'Round' + ' ' + str(rounds[0]['round_number']) + '-' + rounds[0]['round_name'],
                    'fieldname': '',
                    'fieldtype': 'Section Break'
                },
                {
                    'label': 'Date',
                    'fieldname': 'date',
                    'fieldtype': 'Datetime',
                    # 'default': z['date']

                },
                {
                    'label': '',
                    'fieldname': '',
                    'fieldtype': 'Column Break'
                }, 
                {
                    "label": "Interviewers",
                    'fieldname': "interviewers",
                    "fieldtype": "Table MultiSelect",
                    "options": "Interviewer",
                    '_link_field':'employee'
                }
            ]
            list1.append(y)
        rounds_ = [val for sublist in list1 for val in sublist] 
        interviewer = frappe.get_doc('DocType', 'Interviewer')
        return {'rounds':rounds_, 'interviewer': interviewer} 

@frappe.whitelist()
def save_interview_round(formdata, job_applicant):
    data = json.loads(formdata)
  
    job_applicant_doc = frappe.get_doc("Job Applicant", job_applicant)

    job_opening_doc = frappe.get_doc("Job Opening", job_applicant_doc.job_title)

    get_interview = frappe.get_list('Interview', filters={'job_applicant': job_applicant}, as_list=1)

    job_opening = frappe.get_list('Job Opening', filters={'name' : job_opening_doc.name}, fields=['designation'], as_list =1)

    interview_configuration = frappe.get_list('Interview Round Configuration', filters={'parent': job_opening[0][0]}, fields=['round_number', 'round_name'], order_by='round_number')
    interview1 = frappe.get_list('Interview', filters={'job_applicant': job_applicant}, as_list=1)
    print(interview_configuration, len(interview_configuration))
    # configuration = frappe.get_all('Interview Configuration', filters={'designation': job_opening[0][0]})
    # print(len(configuration))
    # if len(configuration) == 0:
    #     return False

    if len(get_interview) == 0:
        interview = frappe.new_doc("Interview")
        interview.job_applicant = job_applicant
        interview.job_opening = job_opening_doc.name
        interview.designation = job_opening_doc.designation
        interview.current_round = interview_configuration[0]['round_name']
        interview.current_round_status = "Scheduled"
        interview.insert(ignore_permissions=True)
    
        interview1 = frappe.get_list('Interview', filters={'job_applicant': job_applicant}, as_list=1)
        interview_round = frappe.new_doc('Interview Round')
        interview_round.interview = interview1[0][0]
        interview_round.job_applicant = job_applicant
        interview_round.job_opening = job_opening_doc.name
        interview_round.designation = job_opening_doc.designation
        interview_round.attached_resume = job_applicant_doc.resume_attachment
        interview_round.round = interview_configuration[0]['round_name']
        interview_round.date = data['date']
        interview_round.round_number = interview_configuration[0]['round_number']
        # interview_round.interviewers = data['interviewers']
        for row in data['interviewers']:
            interview_round.append('interviewers', {
                'employee': row['employee']
            })
        print('==================')    
        interview_round.insert(ignore_permissions=True)

        job_applicant = frappe.get_doc('Job Applicant', job_applicant)
        job_applicant.current_round = 'Round' + " " + interview_configuration[0]['round_number']
        job_applicant.status = 'Round' + " " + interview_configuration[0]['round_number'] + " " + 'Scheduled'    
        job_applicant.save(ignore_permissions=True)
       
        print("Save interview round")

    else:
        existing_rounds_ = frappe.get_list("Interview Round", fields=["round"], filters={
                                'interview': interview1[0][0]}, as_list=1)
        existing_rounds = [i[0] for i in existing_rounds_]
        rounds = frappe.get_list("Interview Round Configuration", fields=['*'], filters={'parent': job_opening_doc.designation, 'round_name': ['not in', existing_rounds]}, order_by='round_number')
       
       
        interview = frappe.get_doc("Interview", get_interview[0][0])
        interview.current_round = rounds[0]['round_name']
        interview.current_round_status = "Scheduled"
        interview.save(ignore_permissions=True)

        interview_round = frappe.new_doc('Interview Round')
        interview_round.interview = get_interview[0][0]
        interview_round.job_applicant = job_applicant
        interview_round.job_opening = job_opening_doc.name
        interview_round.designation = job_opening_doc.designation
        interview_round.attached_resume = job_applicant_doc.resume_attachment
        interview_round.round = rounds[0]['round_name']
        interview_round.date = data['date']
        interview_round.round_number = rounds[0]['round_number']
        # interview_round.interviewers = data['interviewers']
        # interview_round.comments = 
        for row in data['interviewers']:
            interview_round.append('interviewers', {
                'employee': row['employee']
            })
        interview_round.insert(ignore_permissions=True)

        job_applicant = frappe.get_doc('Job Applicant', job_applicant)
        job_applicant.current_round = 'Round' + " " + rounds[0]['round_number']
        job_applicant.status = 'Round' + " " + rounds[0]['round_number'] + " " + 'Scheduled'    
        job_applicant.save(ignore_permissions=True)

def send_mail_to_employees_on_shift():
    now_datetime = frappe.utils.now_datetime()
    from_time = now_datetime.strftime('%H:%m:%S')
    add_one_hour = now_datetime + timedelta(hours=1)
    to_time = add_one_hour.strftime('%H:%m:%S')
    shift = frappe.db.sql("""select name from `tabShift Type` where HOUR(start_time) = %s """,(int(now_datetime.hour) - 1))
    if shift:
        notification = frappe.get_doc('Notification', 'Employees on Shift')
        doc = frappe.get_doc('Shift Type', shift[0][0])
        # doc.from_time = from_time
        # doc.to_time = to_time
        # checkin_frm = frappe.utils.now_datetime().strftime('%Y-%m-%d 00:00:00')
        # checkin_to = frappe.utils.now_datetime().strftime('%Y-%m-%d 23:59:59')
        employees = frappe.get_all('Employee', filters={'default_shift': doc.name,"status":"Active"}, fields=['employee_name','name'])

        query = """select employee,employee_name from `tabEmployee Checkin` where date(time) = '{0}' and shift = '{1}' group by employee """.format(frappe.utils.nowdate(),doc.name)
        debug_data = {'query': query, 'desc': 'description of location of code'}
        frappe.logger().info(debug_data)

        checkin = frappe.db.sql("""select employee,employee_name,time from `tabEmployee Checkin` where date(time) = %s and shift = %s group by employee """ ,(frappe.utils.nowdate(),doc.name),as_dict=1)

        leaves_employees = frappe.get_all('Attendance', filters={'attendance_date': frappe.utils.nowdate() ,'status': 'On Leave'}, fields=['employee','employee_name'] )
        print("checkins = ",checkin)
    # calculating total employees name and count
        if employees:
            emp = {i.name:i.employee_name for i in employees}
            emp_count = len(emp)
            emp_values = [emp[i] for i in emp]
        else:
            emp_count = 0
            emp_values = []
        doc.emp_count = emp_count
        doc.emp_values = emp_values

    # calculating present employees name and count
        if checkin:
            chkn = {i.employee:i.employee_name for i in checkin}
            chkn_count = len(chkn)
            chkn_values = [chkn[i] for i in chkn]
            chkn_time = [i.time.strftime('%Y-%m-%d %H:%m:%S') for i in checkin]
            chkn_lst = []
            for i in chkn_values:
                chkn_lst.append([i,chkn_time[chkn_values.index(i)]])
            
        else:
            chkn={}
            chkn_count = 0
            chkn_list = []
        doc.chkn_count = chkn_count
        doc.chkn_values = chkn_values
        doc.chkn_lst = chkn_lst

    # calculating on leave employees name and count    
        if leaves_employees:
            lv = {i.employee:i.employee_name for i in leave_employees}
            lv_count = len(lv)
            lv_values = [lv[i] for i in lv]
        else:
            lv = {}
            lv_count = 0
            lv_values = []
        doc.lv_count = lv_count
        doc.lv_values = lv_values
        
    # calculating absent employees name and count
        absent = emp.copy()
        for i in list(absent):
            if i in chkn:
                absent.pop(i,None)

        for i in list(absent):
            if i in lv:
                absent.pop(i,None)

        if absent:
            absent_count = len(absent)
            absent_values = [absent[i] for i in absent]

        else:
            absent_count = 0
            absent_values = []   
        doc.absent_count = absent_count
        doc.absent_values = absent_values
        # doc.checkins = checkin
        # doc.employees = employees
        args={'doc': doc}
        recipients, cc, bcc = notification.get_list_of_recipients(doc, args)
        frappe.enqueue(method=frappe.sendmail, recipients=recipients, cc = cc, bcc = bcc, sender=None, 
        subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))

def send_mail_to_employees_on_shift_end():
    now = frappe.utils.now_datetime()
    upto = now.strftime('%H:%M:%S')
    from_time = now - timedelta(hours=1)
    one_hour_before = from_time.strftime('%H:%M:%S')

    # In the below sql command we will be fetching shift type such that time upto which checking out is allowed after shift end, is between
    # current time and one hour before current time
    shift = frappe.db.sql("""select name from `tabShift Type` where ADDTIME(end_time, CONCAT(FLOOR(allow_check_out_after_shift_end_time/60),':',LPAD(MOD(allow_check_out_after_shift_end_time,60),2,'0'),':00.000000'))
     <= %s and ADDTIME(end_time, CONCAT(FLOOR(allow_check_out_after_shift_end_time/60),':',LPAD(MOD(allow_check_out_after_shift_end_time,60),2,'0'),':00.000000')) > %s;""",(upto,one_hour_before))
    if shift:
        notification = frappe.get_doc('Notification', 'Employee on Shift Ends')
        doc = frappe.get_doc('Shift Type', shift[0][0])
        
        query = """Select employee_name, shift, min(time) as checkin, max(time) as checkout From `tabEmployee Checkin` 
        where shift='{0}' and DATE(time) ='{1}' group by employee,DATE(time) order by time desc; """.format(doc.name,frappe.utils.nowdate())
        debug_data = {'query': query, 'desc': 'description of location of code'}
        frappe.logger().info(debug_data)

        checkin = frappe.db.sql("""Select employee_name, shift, min(time) as checkin, max(time) as checkout From `tabEmployee Checkin` 
        where shift=%s and DATE(time) =%s group by employee,DATE(time) order by time desc; """ ,(doc.name,frappe.utils.nowdate()),as_dict=1)

        doc.checkins = checkin
        args={'doc': doc}
        recipients, cc, bcc = notification.get_list_of_recipients(doc, args)
        frappe.enqueue(method=frappe.sendmail, recipients=recipients, cc = cc, bcc = bcc, sender=None, 
        subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))


def change_last_sync_of_checkin():
    shifts = frappe.db.get_list("Shift Type",as_list=1)
    shift_list = []
    for i in shifts:
        for j in i:
            shift_list.append(j)

    for i in shift_list:
        shift = frappe.get_doc("Shift Type",i)
        grace_time = ans = frappe.utils.now_datetime().replace(hour=0,minute=0,second=0,microsecond=0)+shift.end_time + timedelta(minutes=shift.allow_check_out_after_shift_end_time)
        grace_time_int = int(grace_time.strftime("%H%M"))
        cur_time = frappe.utils.now_datetime()
        cur_time_int = int(cur_time.strftime("%H%M"))
        if cur_time_int >= grace_time_int:
            shift.last_sync_of_checkin = cur_time
            shift.save()


@frappe.whitelist()
def maternity_leave_mail():
    date_today = date.today()
    next_month_date = date_today.replace(month = date_today.month +1)
    leaves = frappe.db.get_list("Leave Application",{"to_date":next_month_date,"leave_type":"Maternity Leave"},["employee_name","name"])
    notification = frappe.get_doc('Notification', 'Materinity leave Notification')
    for i in leaves:
        doc = frappe.get_doc('Leave Application', i.name)
        args={'doc': doc}
        # cc, bcc = notification.get_list_of_recipients(doc, args)
        mail_id = frappe.db.get_value("User",{'full_name':i.employee_name},['email'])
        frappe.enqueue(method=frappe.sendmail, recipients=mail_id, sender=None, 
            subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))

def validate_leaves(doc, method):
    leave_details = get_leave_details(doc.employee, doc.posting_date)
    leave_details = frappe._dict(leave_details)
    if 'Annual Leave' in leave_details.leave_allocation:
        remaining_leaves = leave_details.leave_allocation['Annual Leave']['remaining_leaves']

        filters = {
            'employee': doc.employee,
            'leave_type': 'Annual Leave',
            'docstatus': 1
        }
        leave_allocation_list = frappe.db.get_all('Leave Allocation', filters=filters, fields=['from_date', 'to_date', 'new_leaves_allocated', 'total_leaves_allocated'], order_by='name desc') 
        current_year_leaves = leave_allocation_list[0]['new_leaves_allocated']
        previous_leaves = remaining_leaves - current_year_leaves
        num_months = (leave_allocation_list[0]['to_date'].year - leave_allocation_list[0]['from_date'].year) * 12 + (leave_allocation_list[0]['to_date'].month - leave_allocation_list[0]['from_date'].month)
        
        monthly_assign_leave = current_year_leaves / num_months
       
        months = datetime.strptime(doc.from_date, '%Y-%m-%d')
        
        per_month_leaves = 0
        for i in range(leave_allocation_list[0]['from_date'].month, months.month+1):
            per_month_leaves += monthly_assign_leave 
            
        total_allowed_leaves = per_month_leaves + previous_leaves
        # Sauce: https://stackoverflow.com/a/24838652/9403680
        from math import floor
        total_allowed_leaves = floor(total_allowed_leaves * 2) / 2
        if doc.total_leave_days > total_allowed_leaves:
            frappe.throw('You should take only {} leaves in this month'.format((total_allowed_leaves)))             

def formatNumber(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num

def send_probation_peroid_end_notification():
    employees = frappe.db.get_all('Employee', fields=['employee_name', 'date_of_joining', 'name'])
    for employee in employees:
        doj= employee['date_of_joining']
        today = datetime.strptime(frappe.utils.today(), '%Y-%m-%d').date()
        num_months = (today.year - doj.year) * 12 + (today.month - doj.month)
        if num_months == 7:
            notification = frappe.get_doc('Notification', 'Probation Period Completion')
            doc = frappe.get_doc('Employee', employee['name'])
            args={'doc': doc}
            recipients, cc, bcc = notification.get_list_of_recipients(doc, args)
            frappe.enqueue(method=frappe.sendmail, cc=cc, sender=None, 
                subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))
 
