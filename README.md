{% extends 'cbase.html' %}

{% block title %}CREATE CHAT LOBBY{% endblock %}

{% block css %}
<link rel="stylesheet" href="/static/style.css">
<style>
    /* Responsive Design */
    @media screen and (max-width: 768px) {
        .create_lobby a {
            color: rgb(200, 50, 50);
            font-size: 0.9rem;
            /* Slightly reduce font size for tablets */
            /* Adjust color for better visibility */
        }
    }

    @media screen and (max-width: 480px) {
        .create_lobby a {
            color: rgb(220, 60, 60);
            font-size: 0.8rem;
            /* Further reduce font size for mobile */
            padding: 3px;
            /* Adjust padding for smaller screens */
            /* Enhance contrast for smaller devices */
        }

        .create_lobby a:hover {
            color: rgb(141, 18, 18);
            text-decoration: none;
            /* Simplify interaction for smaller devices */
            font-weight: bold;
            /* Add emphasis instead of underline */
        }
    }
</style>
<nav class="flex items-center justify-between px-2 h-12 fixed top-0 w-full">
    <a class="flex text-xl font-serif text-white italic" href="home">AlgoVisualizer</a>
    <div class="relative cursor-pointer" id="dropdownButton">
        <div onclick="toggleDropdown()" class="flex text-white ml-40">
            {% if profile_photo_base64 %}
            <img class="h-10 w-10 rounded-full" src="data:image/jpeg;base64,{{ profile_photo_base64 }}"
                alt="Profile Photo">
            {% else %}
            <img src="/static/profile.png" class="h-10 rounded-full" alt="default Profile Photo">
            {% endif %}
        </div>
        <div id="dropdown" class="dropdown rounded-xl border-2 border-red-900 absolute mt-1 mr-40 hidden">
            <div class="hover:bg-red-900 font-serif text-md w-44 p-3 text-white rounded-xl">
                <a class="p-3 w-44" href="{% if user.is_authenticated %}/profile{% else %}/{% endif %}"> Your
                    Profile</a>
            </div>
            <div class="hover:bg-red-900 font-serif text-md w-44 p-3 text-white rounded-xl">
                <a class="p-3 w-44" href="login">Sign In / Sign Up</a>
            </div>
            <div class="hover:bg-red-900 font-serif text-md w-44 p-3 text-white rounded-xl">
                <a class="p-3 w-44" href="about">Contact Us</a>
            </div>
            <div class="hover:bg-red-900 font-serif text-md w-44 p-3 text-white rounded-xl">
                <a class="p-3 w-44" href="chatlobby">Chat</a>
            </div>
        </div>
    </div>
</nav>
{% endblock %}

    {% block h1 %} Create chat lobby! {% endblock %}
    {% block h4 %} {{message}} {% endblock %}

    {% block div %}

    <form method="post" action="{% url 'lobby' %}"> {% csrf_token %}
        <label class="flex text-lg pl-2" for="name">Enter your user ID name here:</label>
        <input class="h-10 px-2 rounded-md" type="text" id="name" name="name" required>

        <label class="flex text-lg pl-2 rounded-md" for="lobbyCode">Enter lobby code if you got one:</label>
        <input class="h-10 px-2" type="text" id="lobbycode" name="lobbycode" required>

        <button class="bg-red-700 h-10 w-32 my-5 rounded-xl" type="submit">Enter Lobby</button>
    </form>

    <div class="create_lobby ">
        <p class="text-lg">Don't have a lobby code? Well.... <a class="text-red-600 hover:text-red-800 hover:underline"
                href="{% url 'create_lobby' %}">Create your own.</a></p>
    </div>
<script>
    function toggleDropdown() {
        const dropdown = document.querySelector('#dropdown');
        dropdown.classList.toggle('hidden');
    }

    // Close the dropdown if clicked outside
    document.addEventListener('click', function (event) {
        const dropdown = document.querySelector('#dropdown');
        const dropdownButton = document.querySelector('#dropdownButton');

        // Check if the click is outside the dropdown and the button
        if (!dropdownButton.contains(event.target)) {
            dropdown.classList.add('hidden');
        }
    });

    // Hide the dropdown when the page is unloaded (redirected or refreshed)
    window.addEventListener('beforeunload', function () {
        const dropdown = document.querySelector('#dropdown');
        dropdown.classList.add('hidden');
    });
</script>
{% endblock %}
