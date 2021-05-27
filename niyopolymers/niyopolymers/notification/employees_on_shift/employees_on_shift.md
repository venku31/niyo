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

<div class="col-md-4">
<a><b>Present Employees are: <b></a>
<ol>
{% for j in doc.checkins %}
<li>
{{ j.employee_name }}
</li>
{% endfor %}
</ol>
</div>

<div class="col-md-4">
<a><b>Absent Employees are: <b></a>
<ol>
{% for i in non_match %}
<li>
{{ i }}
</li>
{% endfor %}
</ol>
</div>

<div class="col-md-4">
<a><b>Employees that are on leave are: <b></a>
<ol>
{% for i in leaves_employees %}
<li>
{{ i.name }}
</li>
{% endfor %}
</ol>
</div>