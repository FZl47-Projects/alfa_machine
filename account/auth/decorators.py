from functools import wraps
from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def user_role_required_cbv(roles):
    def wrapper(func):
        @wraps(func)
        def inner(self, request, *args, **kwargs):
            user = request.user
            if user is None or user.is_anonymous:
                return redirect('account:login')
            role = user.role
            if not (role in roles):
                return redirect('account:login')
            department = getattr(user,'department',None)
            if department is None:
                return redirect('account:login')
            return func(self, request, *args, **kwargs)

        return inner

    return wrapper
