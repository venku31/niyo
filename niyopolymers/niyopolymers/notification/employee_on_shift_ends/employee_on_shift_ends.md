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

{% if doc.checkins %}
<table>
  <tr>
    <th style="text-align: center">Employee Name</th>
    <th style="text-align: center">Shift</th>
    <th style="text-align: center">Checkin</th>
    <th style="text-align: center">Checkout</th>
  </tr>
  {% for j in doc.checkins %}
  <tr>
    <td style="text-align: center">{{ j.employee_name }}</td>
    <td style="text-align: center">{{ j.shift }}</td>
    <td style="text-align: center">{{ j.checkin.strftime('%Y-%m-%d %H:%M:%S') }}</td>
    <td style="text-align: center">{{ j.checkout.strftime('%Y-%m-%d %H:%M:%S') }}</td>
  </tr>
  {% endfor %}
</table>
{% else %}
<b>No employee checkin checkout found for {{ doc.name }} </b>
{% endif %}