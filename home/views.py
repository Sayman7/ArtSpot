from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils.timezone import now, timedelta
from django.core.cache import cache
from django.conf import settings
from .models import Post, Comment, LikeDislike, Profile, Order, UserProfile
from .forms import UserRegisterForm, PostForm, CommentForm, ProfileUpdateForm
import razorpay
import json
import os
import random, string
import requests

# Homepage / Landing

def index(request):
    return render(request, 'index.html')

def landing(request):
    return render(request, "landing.html")

# Authentication

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("feed")
    return render(request, "login.html", {"form": form})

# Feed

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    if request.method == 'POST':
        if 'content' in request.POST or 'image' in request.FILES:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return render(request, 'single_post.html', {'post': post})
                return redirect("feed")
        elif 'text' in request.POST and 'post_id' in request.POST:
            post_id = request.POST.get('post_id')
            text = request.POST.get('text')
            post = Post.objects.get(id=post_id)
            comment = Comment.objects.create(user=request.user, post=post, text=text)
            return JsonResponse({
                'success': True,
                'username': request.user.username,
                'text': text,
                'comment_count': post.comments.count()
            })
    else:
        form = PostForm()
    return render(request, 'feed.html', {'form': form, 'posts': posts})

# Post Detail

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    profile_user = post.user
    posts = Post.objects.filter(user=profile_user).exclude(id=post.id)[:3]
    source = request.GET.get('from', '')
    show_pay_button = (source == 'feed')
    context = {
        'post': post,
        'profile_user': profile_user,
        'posts': posts,
        'show_pay_button': show_pay_button,
    }
    return render(request, 'post_detail.html', context)

def custom_csrf_failure_view(request, reason=""):
    return redirect('/feed/')

# Like/Dislike

@login_required
def like_dislike_post(request, post_id, action):
    post = get_object_or_404(Post, id=post_id)
    like_dislike, created = LikeDislike.objects.get_or_create(user=request.user, post=post)
    if action == "like":
        like_dislike.like = True
        like_dislike.dislike = False
    elif action == "dislike":
        like_dislike.like = False
        like_dislike.dislike = True
    like_dislike.save()
    likes_count = LikeDislike.objects.filter(post=post, like=True).count()
    dislikes_count = LikeDislike.objects.filter(post=post, dislike=True).count()
    return JsonResponse({"success": True, "likes": likes_count, "dislikes": dislikes_count})

# Comments

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()
            if not text:
                return JsonResponse({"success": False, "error": "Comment cannot be empty!"}, status=400)
            post = get_object_or_404(Post, id=post_id)
            comment = Comment.objects.create(post=post, user=request.user, text=text)
            return JsonResponse({"success": True, "username": request.user.username, "text": comment.text})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON format"}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)

# Profiles

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)
    posts = Post.objects.filter(user=profile_user)
    following = request.user.profile.following.all()
    context = {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "following": following
    }
    return render(request, "profile.html", context)

@login_required
def follow_unfollow(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    profile_to_follow = get_object_or_404(Profile, user=user_to_follow)
    current_user_profile = get_object_or_404(Profile, user=request.user)
    if profile_to_follow != current_user_profile:
        if request.user in profile_to_follow.followers.all():
            profile_to_follow.followers.remove(request.user)
            current_user_profile.following.remove(user_to_follow)
        else:
            profile_to_follow.followers.add(request.user)
            current_user_profile.following.add(user_to_follow)
    followers_count = profile_to_follow.followers.count()
    following_count = current_user_profile.following.count()
    return JsonResponse({
        "following": request.user in profile_to_follow.followers.all(),
        "followers_count": followers_count,
        "following_count": following_count
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

# Posts

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def trending_posts_view(request):
    trending_posts = cache.get('trending_posts')
    if not trending_posts:
        trending_posts = Post.objects.annotate(like_count=Count('likes_dislikes')).order_by('-like_count')[:10]
        cache.set('trending_posts', list(trending_posts), timeout=86400)
    return render(request, 'trending.html', {'trending_posts': trending_posts})

# Search

def search_users(request):
    query = request.GET.get('q', '').strip()
    users = []
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).distinct()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user_data = [
            {"username": user.username, "first_name": user.first_name, "last_name": user.last_name} 
            for user in users
        ]
        return JsonResponse({"users": user_data})
    return render(request, 'search.html', {'users': users, 'query': query})

# AI Image Generation

API_KEY = os.getenv("OPENAI_API_KEY")

def ai_page(request):
    return render(request, "ai.html")

def generate_image(request):
    if request.method == "GET":
        prompt = request.GET.get("prompt", "").strip()
        if not prompt:
            return JsonResponse({"error": "Prompt is required!"}, status=400)
        improved_prompt = f"A high-quality, artistic, step-by-step creation of {prompt}, beginner-friendly, simple strokes, easy to recreate, digital painting, concept art."
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "dall-e-3",
            "prompt": improved_prompt,
            "n": 1,
            "size": "1024x1024"
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            ai_response = response.json()
            image_url = ai_response["data"][0]["url"]
            guide = generate_art_steps(prompt)
            return JsonResponse({"image_url": image_url, "art_guide": guide})
        else:
            return JsonResponse({"error": f"Failed to generate image. API Response: {response.text}"}, status=400)

def generate_art_steps(subject):
    return [
        f"1️⃣ Sketch: Start with a light pencil sketch of {subject}. Focus on proportions.",
        f"2️⃣ Outline: Use a fine pen or brush to define the shape clearly.",
        f"3️⃣ Base Colors: Apply the main colors lightly with a brush or digital tool.",
        f"4️⃣ Shading & Highlights: Add shadows and light to give depth.",
        f"5️⃣ Final Touches: Enhance details and refine edges for a polished look."
    ]

# Payments

def create_payment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    amount = int(post.price * 100)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({"amount": amount, "currency": "INR", "payment_capture": 1})
    return JsonResponse({
        "key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "currency": "INR",
        "order_id": payment["id"],
        "post_title": post.title
    })

def payment_success(request):
    return render(request, "payment_success.html")

# Chat Lobbies

def chatlobby(request):
    return render(request, 'chatlobby.html')

def lobby(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lobby_code = request.POST.get('lobbycode')
        with open("static/lobbies.json") as f:
            lobbies = json.load(f)
        if lobby_code not in lobbies:
            return render(request, 'chatlobby.html', {'message': 'Lobby does not exist.'})
    return render(request, 'lobby.html', {'user_name': name, 'lobbycode': lobby_code, 'room_name': lobbies[lobby_code]})

def create_lobby(request):
    if request.method == 'POST':
        lobby_name = request.POST.get('lobby_name')
        with open("static/lobbies.json") as f:
            lobbies = json.load(f)
        while True:
            lobby_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            if lobby_code not in lobbies:
                break
        lobbies.update({lobby_code: lobby_name})
        with open("static/lobbies.json", "w") as file:
            json.dump(lobbies, file)
        return render(request, 'create_lobby.html', {'lobby_code': lobby_code})
    return render(request, 'create_lobby.html')
