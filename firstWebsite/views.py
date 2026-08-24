import secrets
import uuid

import jwt
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from MyFirstDjangoWebsite import settings
from firstWebsite.decorators import session_login_required
from firstWebsite.download import download_files
from firstWebsite.modals import Faculty, Faculty_participation_data, mooc_course, events, awards_and_achievments, \
    sponsored_research, research_journal, research_conference, research_book, patents, guided, resource, \
    non_teaching_staff, category, department
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
                    user.session_version = uuid.uuid4()
                    user.save()
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
@session_login_required
def edit_profile(request, user_token=-1):
    try:
        if user_token != -1:
            payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
            actual_pk = payload['user_pk']
            faculty_instance = Faculty.objects.get(pk=actual_pk)
        else:
            faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))
        context = {'key': faculty_instance}
        return render(request,'editProfile.html',context=context)
    except Faculty.DoesNotExist:
        error_message = f"User does not exist in database."
        messages.error(request,error_message)
        return render(request,'404.html')

def deleteuser(request):
    if request.method == "POST":

        faculty_pk = request.POST.get('faculty_pk')
        faculty_object = get_object_or_404(Faculty, pk=faculty_pk)
        faculty_object.delete()
        messages.success(request,"User deleted successfully!")

    return redirect(reverse('manage_access'))

forms = [
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
@session_login_required
@ensure_csrf_cookie
def all_forms(request,form_no):
    form_name = ""
    for values in forms:
        if values['no'] == str(form_no):
            form_name = values['form']

    if form_no:
        if 12 > form_no > 0 or form_no == 16:
            form_number = form_no
            secret_key = Faculty.objects.get(pk=request.session.get('user_id'))
            return render(request,'forms.html',{'form_number': form_number, 'value': secret_key, 'form_name': form_name})
        else:
            return render(request, '404.html')
    return render(request,'404.html')

@session_login_required
def fdp(request):
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
    fac_dir_instance = Faculty.objects.values('department').annotate(count=Count('id')).order_by('department')

    fdp_entries = list(Faculty_participation_data.objects.values('email__department').annotate(count=Count('id')))
    mooc_entries = list(mooc_course.objects.values('email__department').annotate(count=Count('id')))
    events_org_entries = list(events.objects.values('email__department').annotate(count=Count('id')))
    faculty_awards_entries = list(awards_and_achievments.objects.values('email__department').annotate(count=Count('id')))
    sponsored_research_entries = list(sponsored_research.objects.values('email__department').annotate(count=Count('id')))
    research_journal_entries = list(research_journal.objects.values('email__department').annotate(count=Count('id')))
    research_conference_entries = list(research_conference.objects.values('email__department').annotate(count=Count('id')))
    research_book_entries = list(research_book.objects.values('email__department').annotate(count=Count('id')))
    patents_entries = list(patents.objects.values('email__department').annotate(count=Count('id')))
    mtech_guided_entries = list(guided.objects.values('email__department').annotate(count=Count('id')))
    resource_person_entries = list(resource.objects.values('email__department').annotate(count=Count('id')))

    total_forms_entries = {
        'fdp_entries' : { choice['email__department']: choice['count'] for choice in fdp_entries },
        'mooc_entries' : { choice['email__department']: choice['count'] for choice in mooc_entries},
        'events_org_entries' : { choice['email__department']: choice['count'] for choice in events_org_entries},
        'faculty_awards_entries' : { choice['email__department']: choice['count'] for choice in faculty_awards_entries},
        'sponsored_research_entries' : { choice['email__department']: choice['count'] for choice in sponsored_research_entries},
        'research_journal_entries' : { choice['email__department']: choice['count'] for choice in research_journal_entries},
        'research_conference_entries' : { choice['email__department']: choice['count'] for choice in research_conference_entries},
        'research_book_entries' : { choice['email__department']: choice['count'] for choice in research_book_entries},
        'patents_entries' : { choice['email__department']: choice['count'] for choice in patents_entries},
        'mtech_guided_entries' : { choice['email__department']: choice['count'] for choice in mtech_guided_entries},
        'resource_person_entries' : { choice['email__department']: choice['count'] for choice in resource_person_entries}
    }
    context = {'dir_ins': fac_dir_instance, 'chartData' : total_forms_entries}
    return render(request, 'index.html', context=context)

@session_login_required
def profile(request):
    value = Faculty.objects.get(pk=request.session.get('user_id'))
    if value.status == "NR":
        messages.info(request,"Welcome Abroad! Please complete your profile to explore more.")
    context = {'data': value}
    return render(request,'profile.html', context=context)

def about(request):
    return render(request,'about.html')


def fac_card_details(request,department_val):
    department_label_to_value = {choice.value: choice.label for choice in department}
    if department_val:
        department_data = Faculty.objects.filter(department = department_val).order_by('name')
        if department_data:
            if 'topLeftBar' in request.session:
                user = request.session.get('topLeftBar')
            else:
                user = None
            context = {'fac_data': department_data,'user': user,'department': department_label_to_value.get(department_val,department_val) }
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
def progressdetails(request, form_no, user_token):
    form_name = ""
    for values in forms:
        if str(values['no_']).replace('.', '_') == form_no:
            form_name = values['form']

    if request.session.get('topLeftBar'): # Why not faculty ?
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        actual_pk = payload['user_pk']
        if form_no == "1_1":
            instance = Faculty.objects.get(pk=actual_pk)
            return render(request,'editProfile.html', context={'key': instance} )
        elif form_no == "1_2":
            instance = non_teaching_staff.objects.get(pk=actual_pk)
        elif form_no == "2":
            instance = Faculty_participation_data.objects.get(pk=actual_pk)
        elif form_no == "3":
            instance = mooc_course.objects.get(pk=actual_pk)
        elif form_no == "4":
            instance = events.objects.get(pk=actual_pk)
        elif form_no == "5":
            instance = awards_and_achievments.objects.get(pk=actual_pk)
        elif form_no == "6":
            instance = sponsored_research.objects.get(pk=actual_pk)
        elif form_no == "7_1":
            instance = research_journal.objects.get(pk=actual_pk)
        elif form_no == "7_2":
            instance = research_conference.objects.get(pk=actual_pk)
        elif form_no == "7_3":
            instance = research_book.objects.get(pk=actual_pk)
        elif form_no == "7_4":
            instance = patents.objects.get(pk=actual_pk)
        elif form_no == "8":
            instance = guided.objects.get(pk=actual_pk)
        elif form_no == "9":
            instance = resource.objects.get(pk=actual_pk)
        else:
            return render(request,'404.html')

        return render(request,
                      'EditFormPreview.html',
                      context={'form_number': form_no, 'data': instance, 'key_id': user_token,'category': category, 'form_name': form_name}
                      )
    else:
        return render(request, '404.html')

def detailed_info_profile(request, user_token):
    if 'user_id' in request.session and 'topLeftBar' in request.session:
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        actual_pk = payload['user_pk']
        faculty = get_object_or_404(Faculty, pk=actual_pk)
        return render(request, 'detailed-info-profile.html', {'faculty': faculty})
    else:
        return render(request, '404.html')
@session_login_required
def back_up_data(request):
    if request.method == 'GET':
        return download_files(request, True)
    else:
        return render(request, '404.html')

@session_login_required
def send_otp(request):
    # 1. Validation and Response
    to_mail = Faculty.objects.values_list('email', flat=True).get(pk=request.session['user_id'])
    if not to_mail:
        return JsonResponse({"error": "Email not found in the session."}, status=400)

    # 2. Cryptographically secure 6-digit OTP generation
    otp = "".join(str(secrets.randbelow(10)) for _ in range(6))
    session_info_obj = json.loads(request.body)
    session_info = session_info_obj.get('session_filter')
    # 3. Django Session Management
    request.session['otp_email'] = to_mail
    request.session['otp_secret'] = otp
    print("OTP is: ",otp)

    # 4. Django Mail Abstraction
    subject = "OTP Verification"
    message = f"OTP to flush data for session {session_info} from your account is: {otp}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [to_mail]

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        return JsonResponse({"message": "OTP sent successfully!"}, status=200)
    except Exception as e:
        return JsonResponse({"error": f"Failed to send email: {str(e)}"}, status=500)

@session_login_required
def verify_otp_and_flush_data(request):
    if request.method == 'POST':
        otp_and_filter = json.loads(request.body)
        if otp_and_filter.get('code') == request.session['otp_secret']:
            session_filter = otp_and_filter.get('session_filter')
            print("Session Filter value is: ", session_filter)
            deleted_count, details = mooc_course.objects.filter(session=session_filter).delete()
            # Faculty_participation_data.objects.filter(session=session_filter).delete()
            # events.objects.filter(session=session_filter).delete()
            # awards_and_achievments.objects.filter(session=session_filter).delete()
            # sponsored_research.objects.filter(session=session_filter).delete()
            # research_journal.objects.filter(session=session_filter).delete()
            # research_conference.objects.filter(session=session_filter).delete()
            # research_book.objects.filter(session=session_filter).delete()
            # patents.objects.filter(session=session_filter).delete()
            # guided.objects.filter(session=session_filter).delete()
            # resource.objects.filter(session=session_filter).delete()
            return JsonResponse({"message": f"Date Flushed Successfully!\nDeleted {deleted_count} records!"}, status=200)
        else:
            return JsonResponse({"error": "Please re-check the OTP and enter the correct OTP!"}, status=400)

    return render(request, '404.html')