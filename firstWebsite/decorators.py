from functools import wraps

from django.shortcuts import redirect

from MyFirstDjangoWebsite import settings


def session_login_required(view_func):
    """
    A custom decorator that checks for a specific key
    to determine if a user is logged in.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # 1. Check for the session key
        # We assume you set request.session['user_id'] or request.session['is_logged_in']
        # upon successful manual login.

        # Check if the 'user_id' is set in the session
        if request.session.get('user_id'):
            # User is "logged in" based on the session key
            return view_func(request, *args, **kwargs)
        else:
            # User is not "logged in", redirect to the login page
            # We use settings.LOGIN_URL for consistency, but you can hardcode a URL too.
            login_url = getattr(settings, 'LOGIN_URL', '/login')
            return redirect(f'{login_url}?next={request.path}')

    return wrapper