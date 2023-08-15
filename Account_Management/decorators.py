from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def is_admin(user):
    return user.is_authenticated and user.is_staff

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_admin(request.user):
            return redirect(reverse('custom-login'))  # Redirect to your custom login page
        return view_func(request, *args, **kwargs)
    return _wrapped_view