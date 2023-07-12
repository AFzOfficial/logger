from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django import forms


from .models import Profile, Log
from .forms import LogForm, SignUpForm



def index(request, page: int = 1):
    # if request.user.is_authenticated:
    logs = Log.objects.all().order_by('-created_at', '-id',)  # [:5]

    form = LogForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()

            messages.success(request, 'Loged.')
            redirect('home')

    paginator = Paginator(logs, 10)

    if page > paginator.num_pages or page < 1:
        raise Http404('This page could not be found!')

    context = {
        "logs": paginator.get_page(page),
        "form": form,
    }

    return render(request, 'logger/index.html', context)
    
    # return render(request, 'logger/log.html')




def log(request, log: int):
    return render(request, 'logger/log.html')




def user_profile(request, username: str):
    # if request.user.is_authenticated:
    user = get_object_or_404(User, username=username)
    logs = Log.objects.filter(user=user).order_by('-created_at', '-id',)
    # logs = get_list_or_404(Log, user=user)

    if request.method == "POST":
        current_user_profile = request.user.profile

        action = request.POST['follow']

        if action == 'unfollow':
            current_user_profile.follows.remove(user.profile)
        elif action == 'follow':
            current_user_profile.follows.add(user.profile)
        else:
            return redirect('home')

        current_user_profile.save()

    return render(request, 'logger/profile.html', {"profile": user.profile, "logs": logs})

    # return redirect('home')




def user_login(request):
    if not request.user.is_authenticated:

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)

            if user != None:
                login(request, user)
                messages.success(request, 'Logged In Successfully.')
                return redirect('home')
            
            else:
                messages.success(request, 'There was an error logging in.')
                return redirect('login')
        

        return render(request, 'logger/auth/login.html')
    
    return redirect('home')



def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully.')
    return redirect('home')




def user_signup(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data('first_name')

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'Register Successfully.')
            return redirect('home')

    return render(request, 'logger/auth/signup.html', {'form': form})