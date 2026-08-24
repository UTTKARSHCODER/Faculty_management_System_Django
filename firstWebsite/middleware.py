from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from firstWebsite.modals import Faculty
from django.contrib import messages


class CustomAuthForceLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')

        if user_id:
            try:
                user = Faculty.objects.get(id=user_id)

                cookie_version = request.session.get('session_version')
                db_version = str(user.session_version)

                if cookie_version != db_version:
                    request.session.flush()
                    messages.warning(request,"Your role have been updated or you were logged out. Please log in again.")
                    return redirect('login')
            except ObjectDoesNotExist:
                request.session.flush()
                messages.warning(request,"User not found!")
                return redirect('login')

        return self.get_response(request)