{% extends 'base.html' %}
{% block content %}
<a href="{{url_for('new')}}">Add a new user</a>
<h1>See all the users!</h1>
{% for user in users %}
   <p>
   {{user.first_name}} {{user.last_name}}
   <br/>
   <a href="{{url_for('edit', id=user.id)}}">Edit a user!</a>
   <form method="POST" action="{{url_for('show', id=user.id)}}?_method=DELETE">
   <input type="submit" value="Delete user!">
   </form>
   </p>
{% endfor %}
{% endblock %}
