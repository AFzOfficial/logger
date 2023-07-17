from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django import forms


from .models import Profile, Log
from .forms import LogForm, SignUpForm, UpdateUserForm, ProfileForm


def index(request, page: int = 1):
    # if request.user.is_authenticated:
    logs = Log.objects.filter(is_reply=False).order_by('-created_at', '-id',)  # [:5]

    form = LogForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()

            # messages.success(request, 'Loged.')
            return redirect('home')

    paginator = Paginator(logs, 10)

    if page > paginator.num_pages or page < 1:
        raise Http404('This page could not be found!')

    context = {
        "logs": paginator.get_page(page),
        "form": form,
    }

    return render(request, 'logger/index.html', context)


def log(request, id: int, page: int = 1):
    if request.user.is_authenticated:
        log = get_object_or_404(Log, id=id)
        replies = log.replies.all().order_by('-created_at', '-id', )

        paginator = Paginator(replies, 10)

        if page > paginator.num_pages or page < 1:
            raise Http404('This page could not be found!')

        form = LogForm(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                reply = form.save(commit=False)
                reply.user = request.user
                reply.is_reply = True
                reply.save()

                log.replies.add(reply)

                return redirect(request.META.get('HTTP_REFERER'))

        return render(request, 'logger/log.html', {'log': log, 'form': form, 'replies': paginator.get_page(page)})

    return redirect('home')


def account_profile(request, username: str, page: int = 1):
    # if request.user.is_authenticated:
    user = get_object_or_404(User, username=username)
    logs = Log.objects.filter(user=user, is_reply=False).order_by('-created_at', '-id',)
    # logs = get_list_or_404(Log, user=user)

    paginator = Paginator(logs, 10)

    if page > paginator.num_pages or page < 1:
        raise Http404('This page could not be found!')

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

    return render(request, 'logger/profile.html', {"profile": user.profile, "logs": paginator.get_page(page)})

    # return redirect('home')


def login_user(request):
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


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out Successfully.')
    return redirect('home')


def signup_user(request):
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


def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        current_user_profile = Profile.objects.get(user__id=request.user.id)

        info_form = UpdateUserForm(
            request.POST or None, request.FILES or None, instance=current_user)
        photo_form = ProfileForm(
            request.POST or None, request.FILES or None, instance=current_user_profile)

        if info_form.is_valid() and photo_form.is_valid():
            info_form.save()
            photo_form.save()
            # login(request, current_user)
            messages.success(request, 'Updated Successfully.')
            return redirect('update_profile')

        return render(request, 'logger/update_user.html', {'info_form': info_form, 'photo_form': photo_form})

    return redirect('home')


def log_like(request, id: int):
    if request.user.is_authenticated:
        log = get_object_or_404(Log, id=id)

        if log.likes.filter(id=request.user.id):
            log.likes.remove(request.user)
        else:
            log.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER'))


def user_followers(request, username: str, page: int = 1):
    user = get_object_or_404(User, username=username)

    return render(request, 'logger/followers.html', {'profile': user.profile})


def user_followings(request, username: str, page: int = 1):
    user = get_object_or_404(User, username=username)

    return render(request, 'logger/followings.html', {'profile': user.profile})


def delete_log(request, id: int):
    if request.user.is_authenticated:
        log = get_object_or_404(Log, id=id)

        if request.user.id == log.user.id:
            log.delete()

            return redirect(request.META.get('HTTP_REFERER'))

    messages.success(request, 'Are You Kidding?')
    return redirect('home')


def edit_log(request, id: int):
    if request.user.is_authenticated:

        log = get_object_or_404(Log, id=id)

        if request.user.id == log.user.id:
            form = LogForm(request.POST or None, instance=log)

            if request.method == "POST":
                if form.is_valid():
                    log = form.save(commit=False)
                    log.user = request.user
                    log.save()

                    messages.success(request, 'Updated.')
                    return redirect('home')

            return render(request, 'logger/edit_log.html', {'form': form})

    messages.success(request, 'Are You Kidding?')
    return redirect('home')


def search_user(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            search = request.POST['search']

            resault = User.objects.filter(username__contains=search)
            return render(request, 'logger/search.html', {'search': search, 'resault': resault})

        return render(request, 'logger/search.html')

    messages.success(request, 'Are You Kidding?')
    return redirect('home')


def about(request):
    return render(request, 'logger/about.html')