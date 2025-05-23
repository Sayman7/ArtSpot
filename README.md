{% extends 'base.html' %}
{% load static %}

{% block content %}
<link rel="stylesheet" href="{% static 'dashboard.css' %}">
<div class="flex flex-col items-center min-h-screen bg-gradient-to-br from-[#0a0a0a] to-[#6a6e70] text-white">
    <!-- Sidebar -->
    <div class="fixed left-4 top-[50%] transform -translate-y-1/2 w-20 h-[60vh] bg-[#141414] bg-opacity-80 backdrop-blur-md rounded-2xl p-4 transition-all duration-500 shadow-lg group hover:w-48 hover:bg-opacity-90">
        <ul class="space-y-4 mt-4 flex flex-col items-start w-full">
            <li onclick="location.href='{% url 'home' %}'" class="flex items-center gap-4 p-3 w-full text-lg rounded-xl cursor-pointer transition-transform hover:bg-white/10 hover:scale-105 relative">
                <i class="fa-solid fa-home"></i> 
                <span class="ml-4 opacity-0 transform translate-x-[-10px] transition-all duration-500 group-hover:opacity-100 group-hover:translate-x-0">Home</span>
            </li>
            <li onclick="window.open('https://chat.whatsapp.com/YOUR_COMMUNITY_LINK', '_blank')" class="flex items-center gap-4 p-3 w-full text-lg rounded-xl cursor-pointer transition-transform hover:bg-white/10 hover:scale-105 relative">
                <i class="fa-solid fa-chain"></i> 
                <span class="ml-4 opacity-0 transform translate-x-[-10px] transition-all duration-500 group-hover:opacity-100 group-hover:translate-x-0">Community</span>
            </li>
            <li onclick="location.href='{% url 'trending_posts' %}'" class="flex items-center gap-4 p-3 w-full text-lg rounded-xl cursor-pointer transition-transform hover:bg-white/10 hover:scale-105 relative">
                <i class="fa-solid fa-bolt"></i> 
                <span class="ml-4 opacity-0 transform translate-x-[-10px] transition-all duration-500 group-hover:opacity-100 group-hover:translate-x-0">Trending</span>
            </li>
            
            <li class="flex items-center gap-4 p-3 w-full text-lg rounded-xl cursor-pointer transition-transform hover:bg-white/10 hover:scale-105 relative">
                <i class="fa-solid fa-comment"></i> 
                <span class="ml-4 opacity-0 transform translate-x-[-10px] transition-all duration-500 group-hover:opacity-100 group-hover:translate-x-0">Message</span>
            </li>
            <li class="flex items-center gap-4 p-3 w-full text-lg rounded-xl cursor-pointer transition-transform hover:bg-white/10 hover:scale-105 relative">
                <i class="fa-solid fa-bars"></i> 
                <span class="ml-4 opacity-0 transform translate-x-[-10px] transition-all duration-500 group-hover:opacity-100 group-hover:translate-x-0">More</span>
            </li>
        </ul>
    </div>

    <!-- Main Content -->
    <div class="ml-28 w-[85%] flex flex-col items-center p-6">
        <!-- Profile Section -->
        <div class="w-2/3 bg-[#1e1e1e] bg-opacity-85 rounded-2xl p-10 flex items-center shadow-lg">
            {% if user.userprofile.profile_photo %}
            <img src="{{ user.userprofile.profile_photo.url }}" alt="Profile Picture"
                 class="w-32 h-32 rounded-full border-2 border-white shadow-md transform hover:scale-110 transition-transform">
            {% else %}
            <img src="/media/default.jpg" alt="Default Profile Picture"
                 class="w-32 h-32 rounded-full border-2 border-white shadow-md transform hover:scale-110 transition-transform">
            {% endif %} 
            <div class="ml-6 text-white">
                <h2 class="text-4xl font-bold">@{{ profile_user.username }}</h2>
                <p class="text-gray-300 text-lg">{{ profile_user.bio }}</p>
                <button onclick="location.href='{% url 'edit_profile' %}'" class="mt-4 px-6 py-2 bg-gray-700 text-white font-bold rounded-full hover:bg-gray-600 transition-all">Edit Profile</button>
                <div class="flex gap-8 mt-4 text-lg font-semibold">
                    <p>Posts: <span class="text-gray-300">{{ posts.count }}</span></p>
                    <p>Followers: <span id="followers-count" class="text-gray-300">{{ profile.followers.count|default:0 }}</span></p>
                    <p>Following: <span id="following-count" class="text-gray-300">{{ profile.following.count|default:0 }}</span></p>
                </div>
            </div>
        </div>

        <!-- Tabs -->
        <div class="flex justify-center gap-6 mt-8">
            <button class="tab active px-6 py-2 border-2 border-white text-white rounded-full hover:bg-gray-700 transition">Posts</button>
            <button class="tab px-6 py-2 border-2 border-white text-white rounded-full hover:bg-gray-700 transition">Spotlight</button>
            <button class="tab px-6 py-2 border-2 border-white text-white rounded-full hover:bg-gray-700 transition">Commented</button>
            <button class="tab px-6 py-2 border-2 border-white text-white rounded-full hover:bg-gray-700 transition">Liked</button>
        </div>

        <!-- Content Grid -->
       <div class="grid grid-cols-3 gap-6 mt-10 pb-20">
            {% for post in posts %}
                <div class="rounded-xl overflow-hidden shadow-lg transform transition-transform hover:scale-105">
                    <img src="{{ post.image.url }}" alt="Post" class="w-full h-64 object-cover">
                </div>
            {% empty %}
                 <p class="text-gray-300 col-span-3">No posts yet.</p>
            {% endfor %}
        </div>
    </div>
</div>

<script>
    function switchTab(tabName) {
        document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));
        document.getElementById(tabName).classList.remove('hidden');
        document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('bg-gray-700'));
        event.target.classList.add('bg-gray-700');
    }
</script>
{% endblock %} 
