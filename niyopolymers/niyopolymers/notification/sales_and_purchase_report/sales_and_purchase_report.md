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
    <th style="text-align: center">Header</th>
    <th style="text-align: center">Total Sales of the day</th>
    <th style="text-align: center">Total Sales till now</th>
    <th style="text-align: center">Total Purchase of the day</th>
    <th style="text-align: center">Total Purchase till now</th>
    <th style="text-align: center">Amount Received Today</th>
    <th style="text-align: center">Amount Paid Today</th>
  </tr>
  <tr>
    <td style="text-align: center">Logic</td>
    <td style="text-align: center">{{ doc.today_sales_invoice }}</td>
    <td style="text-align: center">{{ doc.yearly_sales_invoice }}</td>
    <td style="text-align: center">{{ doc.today_purchase_invoice }}</td>
    <td style="text-align: center">{{ doc.yearly_purchase_invoice }}</td>
    <td style="text-align: center">{{ doc.receive_payment_entry }}</td>
    <td style="text-align: center">{{ doc.pay_payment_entry }}</td>
  </tr>
</table>