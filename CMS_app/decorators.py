from django.shortcuts import redirect
from django.urls import reverse

def unauthenticated_user(view_f):
    def wrapper_f(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('CMS_app:dashboard'))
        else:
            return view_f(request, *args, **kwargs)

    return wrapper_f
