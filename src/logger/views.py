from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Log, Profile
from .decorators import guest_required
from .forms import LogForm, SignUpForm, UpdateUserForm, ProfileForm


def index(request, page: int = 1):
    logs = Log.objects.filter(is_reply=False).order_by('-created_at', '-id',)

    form = LogForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        log = form.save(commit=False)
        log.user = request.user
        log.save()

        return redirect('home', page=page)

    paginator = Paginator(logs, 10)

    return render(request, 'logger/index.html', {"logs": paginator.get_page(page), "form": form})


@login_required
def log(request, id: int, page: int = 1):
    log = get_object_or_404(Log, id=id)
    replies = log.replies.all().order_by('-created_at', '-id', )

    paginator = Paginator(replies, 10)

    form = LogForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        reply = form.save(commit=False)
        reply.user = request.user
        reply.is_reply = True
        reply.save()

        log.replies.add(reply)

        return redirect('log', id=id, page=page)

    return render(request, 'logger/log.html', {'log': log, 'form': form, 'replies': paginator.get_page(page)})


def account_profile(request, username: str, page: int = 1):
    user = get_object_or_404(User, username=username)
    logs = Log.objects.filter(
        user=user, is_reply=False).order_by('-created_at', '-id',)

    paginator = Paginator(logs, 10)

    # if request.method == "POST" and request.user.is_authenticated:
    #     current_user_profile = request.user.profile

    #     action = request.POST['follow']

    #     match action:
    #         case 'unfollow':
    #             current_user_profile.follows.remove(user.profile)
    #         case 'follow':
    #             current_user_profile.follows.add(user.profile)
    #         case _:
    #             return redirect('home')

    #     current_user_profile.save()

    return render(request, 'logger/profile.html', {"profile": user.profile, "logs": paginator.get_page(page)})


@login_required
def follow_user(request, username: str):
    user = get_object_or_404(User, username=username)
    current_user_profile = request.user.profile

    current_user_profile.follows.add(user.profile)
    current_user_profile.save()
    messages.success(request, 'User Followed.')
    return redirect('profile', username=username)


@login_required
def unfollow_user(request, username: str):
    user = get_object_or_404(User, username=username)
    current_user_profile = request.user.profile

    current_user_profile.follows.remove(user.profile)
    current_user_profile.save()
    messages.success(request, 'User Unfollowed.')
    return redirect('profile', username=username)



@guest_required
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            messages.success(request, 'Logged In Successfully.')
            return redirect('home')

        messages.success(request, 'There was an error logging in.')
        return redirect('login')

    return render(request, 'logger/auth/login.html')


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out Successfully.')
    return redirect('home')


@guest_required
def signup_user(request):
    form = SignUpForm(request.POST or None)

    if User.objects.all().count() > 99:
        messages.success(
            request, 'Sorry Registration has reached its maximum.')
        return redirect('home')

    if request.method == "POST" and form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(
            request, username=username, password=password)
        login(request, user)
        messages.success(request, 'Registered Successfully.')
        return redirect('home')

    return render(request, 'logger/auth/signup.html', {'form': form})


@login_required
def update_profile(request):
    current_user = User.objects.get(id=request.user.id)

    info_form = UpdateUserForm(
        request.POST or None, request.FILES or None, instance=current_user)
    profile_form = ProfileForm(
        request.POST or None, request.FILES or None, instance=current_user.profile)

    if request.method == "POST":
        if info_form.is_valid() and profile_form.is_valid():
            info_form.save()
            profile_form.save()
            # login(request, current_user)
            messages.success(request, 'Updated Successfully.')
    return render(request, 'logger/update_user.html', {'info_form': info_form, 'profile_form': profile_form})


@login_required
def log_like(request, id: int):
    log = get_object_or_404(Log, id=id)

    if log.likes.filter(id=request.user.id):
        log.likes.remove(request.user)
    else:
        log.likes.add(request.user)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def user_followers(request, username: str, page: int = 1):
    user = get_object_or_404(User, username=username)
    followers = user.profile.followed_by.all()
    paginator = Paginator(followers, 100)
    return render(request, 'logger/followers.html', {'profile': user.profile, 'followers': paginator.get_page(page)})


@login_required
def user_followings(request, username: str, page: int = 1):
    user = get_object_or_404(User, username=username)
    followings = user.profile.follows.all()
    paginator = Paginator(followings, 100)
    return render(request, 'logger/followings.html', {'profile': user.profile, 'followings': paginator.get_page(page)})


@login_required
def delete_log(request, id: int):
    log = get_object_or_404(Log, id=id)

    if request.user.id == log.user.id:
        log.delete()

        return redirect(request.META.get('HTTP_REFERER'))

    messages.success(request, 'Error when deleting log!')


@login_required
def edit_log(request, id: int):
    log = get_object_or_404(Log, id=id)
    form = LogForm(request.POST or None, instance=log)

    if request.user.id != log.user.id:
        messages.success(request, 'Error when updating log!')
        return redirect('home')

    if request.method == "POST" and form.is_valid():
        log = form.save(commit=False)
        log.user = request.user
        log.save()

        messages.success(request, 'Updated Successfully.')
        return redirect('home')

    return render(request, 'logger/edit_log.html', {'form': form})


@login_required
def search_user(request, page: int = 1):
    search = request.GET.get('query', None)

    if search != None:
        resault = User.objects.filter(
            username__icontains=search).order_by('id', )
        paginator = Paginator(resault, 100)

        return render(request, 'logger/search.html', {'search': search, 'resault': paginator.get_page(page)})

    return render(request, 'logger/search.html')
