{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h2>Edit Your Profile</h2>
    <form method="POST" enctype="multipart/form-data">
        {% csrf_token %}
        
        <label for="username">Username:</label>
        <input type="text" name="username" id="username" value="{{ user.username }}" required>

        <label for="email">Email:</label>
        <input type="email" name="email" id="email" value="{{ user.email }}" required>

        <label for="phone">Phone Number:</label>
        <input type="text" name="phone" id="phone" value="{{ user.userprofile.phone|default:'' }}" placeholder="Enter your phone number">

        <label for="name">Full Name:</label>
        <input type="text" name="name" id="name" value="{{ user.userprofile.name|default:'' }}" placeholder="Enter your full name">

        <label for="profile_photo">Profile Photo:</label>
        <input type="file" name="profile_photo" id="profile_photo">

        {% if user.userprofile.profile_photo %}
            <p>Current Photo:</p>
            <img src="{{ user.userprofile.profile_photo.url }}" alt="Profile Photo" width="100">
        {% endif %}

        <button type="submit">Update Profile</button>
    </form>
</div>
{% endblock %}
