from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .forms import SignupForm, ProfileForm
from kover.models import User, Profile
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views import View

# Create your views here.


def login_main(request):
    users = User.objects.filter(user=request.user)
    users = users[0]
    if users:
        url = ''
    else:
        url = '/login/settings/'
    ctx = {
        'user': users,
        'url': url
    }
    return render(request, 'login/login_base.html', ctx)


def login_select(request):
    return render(request, 'login/login_select.html')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
            next_url = request.GET.get('next') or 'settings'
            return redirect('login:settings')
    else:
        form = SignupForm()
    return render(request, 'login/signup.html', {
        'form': form
    })


@login_required
def settings(request):
    username = Profile.objects.filter(user=request.user)
    if username:
        username = username[0]
    else:
        username = 0

    ctx = {
        'username': username
    }
    return render(request, 'login/settings.html', ctx)


@ method_decorator(csrf_exempt)
def nickname(request):
    if request.method == 'GET':
        return render(request, 'login/settings.html')
    elif request.method == 'POST':
        users = request.user
        request = json.loads(request.body)
        name = request['name']
        profiles = Profile.objects.all()
        nicknames = []
        validation = False

        for profile in profiles:
            nicknames.append(profile.nickname)

        if name not in nicknames:
            validation = True
        if validation:
            profile = Profile(
                user=users,
                nickname=name,
            )
            profile.save()
            return JsonResponse({'name': name})
        else:
            return JsonResponse({'name': validation})


# def personal_inf(request):
#     username = Profile.objects.filter(user=request.user)
#     if username:
#         username = username[0]
#     else:
#         username = 0

#     ctx = {
#         'username': username
#     }
#     return render(request, 'login/personal_inf.html', ctx)


def personal_inf(request):
    username = Profile.objects.filter(user=request.user)
    
    ctx = {
        'username': username
    }
    if request.method == 'POST':
        user_change_form = ProfileForm(request.POST, instance=request.user)

        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return render(request, 'login/personal_inf.html', ctx)
    else:
        user_change_form = ProfileForm(instance=request.user)
        return render(request, 'login/personal_inf.html', {'user_change_form': user_change_form})


