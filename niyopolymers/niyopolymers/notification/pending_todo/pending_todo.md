<h2> The below ToDo list are pending...</h2>
{% for i in doc.todos %}
<ol> <a href="{{ frappe.utils.get_url(doc.get_url()) }}">{{ i.description }} </a> </ol>
{% endfor %}