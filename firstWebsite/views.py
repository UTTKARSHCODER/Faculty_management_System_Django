from functools import wraps

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from MyFirstDjangoWebsite import settings
from firstWebsite.modals import Faculty, Faculty_participation_data, mooc_course, events, awards_and_achievments, \
    sponsored_research, research_journal, research_conference, research_book, patents, guided, resource, \
    non_teaching_staff, category
from .modals import Student_Directory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


CLIENT_ID = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
@csrf_exempt
def gsi_verify_login(request):
    """Handles the JWT token received from the Google Sign-In button."""

    global User
    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            id_token_jwt = data.get('id_token')
            users_post = data.get('post_value')

            if not id_token_jwt:
                return JsonResponse({'success': False, 'error': 'No ID token provided.'}, status=400)

            idinfo = id_token.verify_oauth2_token(
                id_token_jwt,
                google_requests.Request(),
                CLIENT_ID,  # Use your Client ID here
                clock_skew_in_seconds = 10
            )

            email = idinfo.get('email')

            try:
                if email.endswith('@skit.ac.in'):
                    if users_post == 'spa' or users_post == 'ad' or users_post == 'fa':
                        User = Faculty
                        user = Faculty.objects.get(email=email,role__iexact=users_post)
                    else:
                        User = None
                        user = None
                    # If login is successful:
                    request.session['user_id'] = user.pk
                    request.session['topLeftBar'] = users_post
                    request.session['session_version'] = str(user.session_version)
                    messages.success(request,"Logged in successfully!")
                    return JsonResponse({
                        'success': True,
                        'redirect_url': '/profile'  # Redirect to the home or dashboard page
                    })
                else:
                    error_message = f"Access denied: Only institutional mails are allowed."

                    # You can optionally add a Django message for standard page rendering
                    messages.error(request, error_message)

                    return JsonResponse({
                        'success': False,
                        'error': error_message
                    }, status=403)
            except User.DoesNotExist:

                error_message = f"Access denied: The email '{email}' is not authorized to log in with selected post."


                return JsonResponse({
                    'success': False,
                    'error': error_message
                }, status=403)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON body.'}, status=400)
        except Exception as e:
            # Handle user restriction error from your custom allauth adapter, etc.
            return JsonResponse({'success': False, 'error': str(e)}, status=401)

    return JsonResponse({'success': False, 'error': 'Invalid method.'}, status=405)


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

@session_login_required
def edit_profile(request):
    try:
        faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))
        context = {'key': faculty_instance}
        return render(request,'editProfile.html',context=context)
    except Faculty.DoesNotExist:
        error_message = f"User does not exist in database."
        messages.error(request,error_message)
        return render(request,'index.html')

def successfulsubmission(request):
    return render(request,'submitSuccess.html')


def deleteuser(request):
    if request.method == "POST":

        faculty_id = request.POST.get('faculty_emp_id')
        faculty_object = get_object_or_404(Faculty, emp_id=faculty_id)
        faculty_object.delete()
        messages.success(request,"User deleted successfully!")

    return redirect(reverse('manage_access'))

@session_login_required
@ensure_csrf_cookie
def all_forms(request,pk):
    if pk:
        if 12 > pk > 0 or pk == 16:
            form_number = pk
            secret_key = Faculty.objects.get(pk=request.session.get('user_id'))
            return render(request,'forms.html',{'form_number': form_number, 'value': secret_key})
        else:
            return render(request, '404.html')
    return render(request,'404.html')

@session_login_required
def fdp(request):
    forms = [
        {'no': '1.1','no_': '1.1', 'form': "Faculty Profile Details", 'tooltip': "Faculty basic details, higher studies, personal file information."},
        {'no': '16','no_': '1.2', 'form': "Non-teaching Staff Profile Details", 'tooltip': "Non-Teaching Staff basic details, higher studies, personal file information."},
        {'no': '1', 'no_': '2','form': "Faculty Participation", 'tooltip': "Faculty participation in FDP, Conference, Workshop, STTP, Seminar etc."},
        {'no': '2', 'no_': '3','form': "MOOC's/Short Term Course/Course Completion", 'tooltip': "MOOCs (Swayam/NPTEL),courses from Infosys Springboard, Coursera, edX, Udemy etc. and other certifications."},
        {'no': '3', 'no_': '4','form': "Events Organized by Department", 'tooltip': "Sponsored/Non Sponsored events organized by department for students, faculty and non- teaching staff."},
        {'no': '4', 'no_': '5', 'form': "Faculty Awards and Achievements", 'tooltip': "Award in Education/Research/Sports, Best paper award, Topper/Gold/Sliver/Elite in SWAYAM/NPTEL courses, Top performing mentors etc."},
        {'no': '5', 'no_': '6','form': "Sponsored Research/Grant Received/Consultancy", 'tooltip': "Sponsored Research/Grant Received/Consultancy"},
        {'no': '6', 'no_': '7.1','form': "Research Publication - Journals", 'tooltip': "Publication in Journal (Faculty and SKIT student)"},
        {'no': '7', 'no_': '7.2','form': "Research Publication - Conference Publication", 'tooltip': "Publication in Conference (Faculty and SKIT student )"},
        {'no': '8', 'no_': '7.3','form': "Research Publication - Book and Book Chapters", 'tooltip': "Author/Editor of a book or author of book chapter (Faculty and SKIT student)"},
        {'no': '9', 'no_': '7.4','form': "Patents", 'tooltip': "Details of Patents published and granted (Faculty and SKIT student)"},
        {'no': '10', 'no_': '8','form': "M.Tech/Ph.D Guided", 'tooltip': "Details of Ph.D and M.Tech students guided by faculty members."},
        {'no': '11', 'no_': '9','form': "Resource Person", 'tooltip': "Session chair or keynote speaker in conference, delivered expert lecture, speaker in FDP, trainer etc."},
    ]
    return render(request, 'fdp_forms.html',context={'values': forms})

@session_login_required
def custom_logout(request):
    if 'user_id' in request.session and 'topLeftBar' in request.session:
        del request.session['user_id']
        del request.session['topLeftBar']
        return redirect(reverse('home'))
    return render(request,"404.html")

# Create your views here.

def index(request):
    fac_dir_instance = Faculty.objects.values('department').annotate(
        count=Count('id')
    ).order_by('department')
    context = {'dir_ins': fac_dir_instance}
    return render(request, 'index.html', context=context)

def student(request):
    stu_dir_instance = Student_Directory.objects.values('batch').annotate(
        count=Count('id')
    ).order_by('batch')
    context = {'dir_ins':stu_dir_instance}
    return render(request, 'student_card_details.html',context = context)

@session_login_required
def profile(request):
    value = Faculty.objects.get(pk=request.session.get('user_id'))
    if value.status == "NR":
        messages.info(request,"Welcome Abroad! Please complete your profile to explore more.")
    context = {'data': value}
    return render(request,'profile.html', context=context)


@session_login_required
def student_directory(request):
    modal = request.session.get('topLeftBar')
    stu_data = Student_Directory.objects.all()
    context = {'stu_data': stu_data, 'user': modal}
    return render(request,'student_directory.html',context = context)

def about(request):
    return render(request,'about.html')

@session_login_required
def stu_card_details(request,pk):
    if pk:
        batches = Student_Directory.objects.filter(batch = pk)
        if batches:
            context = {'stu_data': batches }
            return render(request,'batch_details.html',context=context)
        else:
            messages.info(request,"No data to display")
            return render(request,'index.html')
    return render(request,'404.html')

def fac_card_details(request,pk):
    if pk:
        department = Faculty.objects.filter(department = pk)
        if department:
            if 'topLeftBar' in request.session:
                user = request.session.get('topLeftBar')
            else:
                user = None
            context = {'fac_data': department,'user': user }
            return render(request,'faculty_details.html',context=context)
        else:
            return render(request,'index.html')
    return render(request,'404.html')

def login_page(request):
    return render(request,'login.html')


@session_login_required
def manage_access(request):
    if 'user_id' in request.session and 'topLeftBar' in request.session:
        modal = request.session.get('topLeftBar')
        if modal == 'spa':
            value = Faculty.objects.all()
            context = { 'data': value }
            return render(request,'manage_access.html',context=context)
        else:
            return render(request,'404.html')
    messages.info(request,"User does not exist!")
    return render(request,'index.html')

@session_login_required
def faculty_report(request):
    modal = request.session.get('topLeftBar')
    registerd_faculties = Faculty.objects.filter(status="R")
    context = {'rf' : registerd_faculties, 'user': modal}
    return render(request,'faculty_report.html',context)


def faq(request):
    return render(request,'FaQ.html')

def page_under_construction(request):
    return render(request,'page_under_construction.html')

def cookie_not_found(request):
    return render(request,'403.html')

@session_login_required
def progressdetails(request,pk,key_id):
    if request.session.get('topLeftBar') == 'spa' or request.session.get('topLeftBar') == 'ad':
        if pk == "0":
            non_teaching = non_teaching_staff.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk, 'data': non_teaching,'key_id':int(key_id), 'category' : category})
        elif pk == "1":
            faculty_participation_instance = Faculty_participation_data.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': faculty_participation_instance,'key_id':int(key_id), 'category' : category})
        elif pk == "2":
            mooc_instance = mooc_course.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': mooc_instance,'key_id':int(key_id), 'category' : category})
        elif pk == "3":
            events_instance = events.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': events_instance,'key_id':int(key_id), 'category' : category})
        elif pk == "4":
            awards = awards_and_achievments.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': awards,'key_id':int(key_id), 'category' : category})
        elif pk == "5":
            sponsor = sponsored_research.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': sponsor,'key_id':int(key_id), 'category' : category})
        elif pk == "6":
            research_journal_instance = research_journal.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': research_journal_instance,'key_id':int(key_id), 'category' : category})
        elif pk == "7":
            research_confernce_instance = research_conference.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': research_confernce_instance,'key_id':int(key_id), 'category' : category})
        elif pk == "8":
            research_book_instance = research_book.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': research_book_instance,'key_id':int(key_id), 'category' : category})
        elif pk == "9":
            patents1 = patents.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': patents1,'key_id':int(key_id), 'category' : category})
        elif pk == "10":
            guided1 = guided.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': guided1,'key_id':int(key_id), 'category' : category})
        elif pk == "11":
            resouce_person = resource.objects.get(pk=key_id)
            return render(request, 'progressDetails.html', context={'form_number': pk,'data': resouce_person,'key_id':int(key_id), 'category' : category})
        else:
            return render(request,'404.html')
    else:
        return render(request, '404.html')

def detailed_info_profile(request, faculty_id):
    faculty = get_object_or_404(Faculty, pk=faculty_id)
    return render(request, 'detailed-info-profile.html', {'faculty': faculty})

def add_student(request):
    if request.method == "POST":
        new_mail = request.POST.get('new_email')
        if Student_Directory.objects.filter(email=new_mail).exists():
            messages.error(request, "Email already exists!")
            return redirect(reverse("student-directory"))

        return render(request, 'page_under_construction.html')
    else:
        return render(request,'404.html')

def detailed_info_profile(request, faculty_id):
    if 'user_id' in request.session and 'topLeftBar' in request.session:
        faculty = get_object_or_404(Faculty, pk=faculty_id)
        return render(request, 'detailed-info-profile.html', {'faculty': faculty})
    else:
        return render(request, '404.html')