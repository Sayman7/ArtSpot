
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Get data from form
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        profile_photo = request.FILES.get('profile_photo')

        # Update User model
        user = request.user
        user.username = username
        user.email = email
        user.save()

        # Update UserProfile model
        user_profile.phone = phone
        user_profile.name = name
        if profile_photo:
            user_profile.profile_photo = profile_photo
        user_profile.save()

        return redirect('profile', username=user.username)  # Pass username argument

    return render(request, 'edit.html', {'user': request.user})
