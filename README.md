{% extends 'base.html' %}

{% block content %}
<div class="mx-auto px-4 bg-black pb-6 min-h-screen">

    <style>
        .tooltip-btn {
            position: relative;
        }

        .tooltip-btn:hover .tooltip-text {
            opacity: 1;
            visibility: visible;
        }

        .tooltip-text {
            position: absolute;
            bottom: 135%;
            left: 50%;
            transform: translateX(-50%);
            background-color: #1f2937;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            white-space: nowrap;
            font-weight: bold;
            font-size: 0.75rem;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s;
            z-index: 10;
        }
    </style>

    <!-- Trending Section -->
    <h2 class="text-center text-white text-4xl font-extrabold py-3 pb-8">🔥 Trending Posts</h2>
    <div class="flex justify-center items-center">
        <div class="w-[40rem] pb-10" id="trending-container">
            {% for post in trending_posts %}
            <div class="bg-gray-900 border border-gray-800 rounded-xl shadow-lg p-4 relative flex flex-col my-5">
                <span class="absolute top-2 left-2 bg-yellow-500 text-black px-3 py-1 rounded-full font-bold">#{{ forloop.counter }}</span>

                <!-- Clickable Post Image -->
                <a href="{% url 'post_detail_view' post.id %}" class="rounded-lg overflow-hidden flex justify-center">
                    <img src="{{ post.image.url }}"
                        class="max-w-[23rem] object-cover rounded-lg hover:scale-105 transition">
                </a>

                <div class="mt-4 flex flex-col flex-grow">
                    <div class="flex justify-between items-center mb-2">
                        <a href="{% url 'profile' post.user.username %}" class="text-blue-400 font-semibold">
                            @{{ post.user.username }}
                        </a>
                    </div>

                    <h3 class="text-xl font-bold text-white">
                        <a href="{% url 'post_detail_view' post.id %}" class="hover:text-blue-400">
                            {{ post.title }}
                        </a>
                    </h3>
                    <p class="text-gray-400 text-sm">Category: {{ post.category }}</p>
                    <p class="text-gray-400 text-sm">Price: ₹{{ post.price }}</p>
                    <p class="text-gray-300 mt-2">{{ post.caption }}</p>
                    <p class="text-gray-400 text-sm">Uploaded on: {{ post.created_at|date:"F d, Y" }}</p>

                    <!-- Trending Badge -->
                    <span class="bg-red-500 text-white px-3 py-1 rounded-full text-sm mt-2">🔥 Trending</span>
                </div>
            </div>
            {% empty %}
            <p class="text-center text-gray-300">No trending posts available.</p>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
