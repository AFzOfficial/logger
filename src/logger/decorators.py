from django.shortcuts import redirect

def guest_required(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect('home')
    return wrapper
