{% set leaves_employees = frappe.get_all('Attendance', filters={'attendance_date': frappe.utils.nowdate() ,'status': 'On Leave'}, fields=['name'] ) %}
{% set employees_list = [] %}
    {% for i in doc.employees %}
    {% set a = employees_list.append(i.employee_name) %}
    {% endfor %}

{% set checkins_list = [] %}
    {% for i in doc.checkins %}
    {% set a = checkins_list.append(i.employee_name) %}
    {% endfor %}

{% set non_match = [] %}
{% for i in employees_list %}
{% if i not in checkins_list %}
{% set b = non_match.append(i) %}
{% endif %}
{% endfor %}
<h2>Dashboard</h2>

<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
<table>
  <tr>
    <th style="text-align: center">Shift Name</th>
    <th style="text-align: center">Shift Employees</th>
    <th style="text-align: center">Present</th>
    <th style="text-align: center">Absent</th>
    <th style="text-align: center">On Leave</th>
  </tr>
  <tr>
    <td style="text-align: center">{{ doc.name }}</td>
    <td style="text-align: center">{{ doc.employees|length }}</td>
    <td style="text-align: center">{{ doc.checkins|length }}</td>
    <td style="text-align: center">{{ (doc.employees|length - doc.checkins|length )-leaves_employees|length }}</td>
    <td style="text-align: center">{{ leaves_employees|length }}</td>
  </tr>
</table>

<br>
<p><b>Present Employees</b></p>
<table>
  <tr>
    <th style="text-align: center">Employee Name</th>
    <th style="text-align: center">Shift Incharge</th>
    <th style="text-align: center">Reporting manager</th>
  </tr>
  {% for j in doc.checkins %}
  <tr>
    <td style="text-align: center">{{ j.employee_name }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":j.employee_name},["reporting_manager"]) }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":j.employee_name},["shift_incharge_name"]) }}</td>
  </tr>
  {% endfor %}
</table>


<br>
<p><b>Absent Employees</b></p>
<table>
  <tr>
    <th style="text-align: center">Employee Name</th>
    <th style="text-align: center">Shift Incharge</th>
    <th style="text-align: center">Reporting manager</th>
  </tr>
  {% for i in non_match %}
  <tr>
    <td style="text-align: center">{{ i }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":i},["reporting_manager"]) }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":i},["shift_incharge_name"]) }}</td>
  </tr>
  {% endfor %}
</table>

<br>
<p><b>Employees on leave</b></p>
<table>
  <tr>
    <th style="text-align: center">Employee Name</th>
    <th style="text-align: center">Shift Incharge</th>
    <th style="text-align: center">Reporting manager</th>
  </tr>
  {% for i in leaves_employees %}
  <tr>
    <td style="text-align: center">{{ i.name }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":i.name},["reporting_manager"]) }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":i.name},["shift_incharge_name"]) }}</td>
  </tr>
  {% endfor %}
</table>