Alert! The below employees has been on Leave for 5 consecutive days.
{% for i in doc['employees'] %}
<ol>{{ i['employee'] }}</ol>
{% endfor %}