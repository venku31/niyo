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
    <td style="text-align: center">{{ doc.emp_count}}</td>
    <td style="text-align: center">{{ doc.chkn_count }}</td>
    <td style="text-align: center">{{ doc.absent_count }}</td>
    <td style="text-align: center">{{ doc.lv_count }}</td>
  </tr>
</table>

<br>
<p><b>Present Employees</b></p>
<table>
  <tr>
    <th style="text-align: center">Employee Name</th>
    <th style="text-align: center">Shift Incharge</th>
    <th style="text-align: center">Reporting manager</th>
    <th style="text-align: center">Checkin Time</th>
  </tr>
  {% for j in doc.chkn_lst %}
  <tr>
    <td style="text-align: center">{{ j[0] }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":j[0]},["reporting_manager"]) }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":j[0]},["shift_incharge_name"]) }}</td>
    <td style="text-align: center">{{ j[1] }}</td>
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
  {% for i in doc.absent_values %}
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
  {% for i in doc.lv_values %}
  <tr>
    <td style="text-align: center">{{ i.name }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":i.name},["reporting_manager"]) }}</td>
    <td style="text-align: center">{{ frappe.db.get_value("Employee",{"employee_name":i.name},["shift_incharge_name"]) }}</td>
  </tr>
  {% endfor %}
</table>