from functools import wraps
from django.shortcuts import redirect


def requires_permission(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login')
            if not request.user.has_perm(permission):
                return redirect('authentication:permission-denied')
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def not_logged_in(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request,*args, **kwargs)
        return redirect('management:core:dashboard')
    return wrapper