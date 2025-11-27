from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.views import redirect_to_login

def role_required(*roles):

    def outer(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if getattr(request.user, "is_disabled", False):
                return HttpResponseForbidden("Account disabled by admin.")
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if getattr(request.user, "role", None) not in roles:
                return HttpResponseForbidden("Insufficient permissions for this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return outer