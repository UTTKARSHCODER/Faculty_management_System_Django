import base64
import io
from functools import wraps

from django.contrib import messages
from django.db.models import Count
from django.forms import model_to_dict
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from tablib import Dataset
import pandas as pd

from MyFirstDjangoWebsite import settings
from firstWebsite.modals import Faculty, Faculty_participation_data, mooc_course, events, \
    awards_and_achievments, sponsored_research, research_journal, research_conference, research_book, patents, guided, \
    resource, non_teaching_staff, category as cat
from .modals import Student_Directory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
                CLIENT_ID  # Use your Client ID here
            )

            email = idinfo.get('email')

            try:
                if email.endswith('@skit.ac.in'):
                    if users_post == 'spa' or users_post == 'ad' or users_post == 'fa':
                        User = Faculty
                        user = Faculty.objects.get(email=email,role__iexact=users_post)
                    elif users_post == 'student':
                        User =Student_Directory
                        user = Student_Directory.objects.get(email=email)
                    else:
                        User = None
                        user = None
                    # If login is successful:
                    request.session['user_id'] = user.pk
                    request.session['topLeftBar'] = users_post
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

                # You can optionally add a Django message for standard page rendering
                messages.error(request, error_message)

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
            login_url = getattr(settings, 'LOGIN_URL', '/login/')
            return redirect(f'{login_url}?next={request.path}')

    return wrapper


def save_all_forms(request, pk):
    if request.method == 'POST':
        session = request.POST.get('sessionyear')
        faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))
        if pk == 0:
            name = request.POST.get('name')
            mobile_no = request.POST.get('mobile_no')
            # email = request.POST.get('name')
            department = request.POST.get('department')
            lab_no = request.POST.get('lab_no')
            designation = request.POST.get('designation')
            emp_id = request.POST.get('emp_id')
            highest_qual = request.POST.get('highest_qualification')
            university_name = request.POST.get('univ_name')
            pshd = request.POST.get('pshd')
            professional_course = request.POST.get('optradio')
            pan_no = request.POST.get('pan_no')
            dob = request.POST.get('dob')
            joining_date = request.POST.get('jd')
            promotion_date = request.POST.get('pd')
            if promotion_date == '':
                promotion_date = None
            joining_report = request.FILES.get('jr')
            offer_letter = request.FILES.get('ol')
            higher_degree_certificate = request.FILES.get('hdc')
            salary_slip = request.FILES.get('ss')
            certificate = request.FILES.get('awards')
            obj = non_teaching_staff(name=name, mobile_no=mobile_no, email=faculty_instance, department=department, Lab_no=lab_no, designation=designation, emp_id=emp_id, highest_qual=highest_qual, university_name=university_name, pshd=pshd, professional_course=professional_course, pan_no=pan_no,dob=dob, joining_date=joining_date, promotion_date=promotion_date, joining_report=joining_report, offer_letter=offer_letter, higher_degree_certificate=higher_degree_certificate, salary_slip=salary_slip, certificate=certificate)
            obj.save()
        elif pk == 1:
            category = request.POST.get('category')
            top = request.POST.get('top')
            mode = request.POST.get('optradio')
            level = request.POST.get('optradio1')
            organizer = request.POST.get('organizer')
            sponser = request.POST.get('sponser')
            approval = request.POST.get('optradio2')
            begi_date = request.POST.get('begi_date')
            end_date = request.POST.get('end_date')
            num_of_days = request.POST.get('num_of_days')
            proof_approval = request.POST.get('optradio3')
            proof_file_path = request.FILES.get('proof_file')
            obj1 = Faculty_participation_data(category=category,top=top,mode=mode,level=level,organizer=organizer,sponsors=sponser,approval=approval,begi_date=begi_date,end_date=end_date,session=session,no_of_days=num_of_days,proof_enclosed=proof_approval,proof_file=proof_file_path,email=faculty_instance)
            obj1.save()
        elif pk == 2:
            category = request.POST.get('category')
            timeline = request.POST.get('toc')
            noc = request.POST.get('noc')
            doc = request.POST.get('optradio3')
            begi_date = request.POST.get('begi_date')
            end_date = request.POST.get('end_date')
            offer = request.POST.get('ofo')
            ctype = request.POST.get('optradio1')
            topper_in = request.POST.get('optradio2')
            remarks = request.POST.get('remarks')
            proof_file = request.FILES.get('proof_file')
            obj2 = mooc_course(category=category,timeline=timeline,noc=noc,doc=doc,begi_date=begi_date,end_date=end_date,offer=offer,ctype=ctype,topper_in=topper_in,session=session,remarks=remarks,proof_file=proof_file,email=faculty_instance)
            obj2.save()
        elif pk == 3:
            category = request.POST.get('category')
            eof = request.POST.get('optradio3')
            topdpo = request.POST.get('topdpo')
            nop = request.POST.get('nop')
            adcc = request.POST.get('adcc')
            ct = request.POST.get('optradio1')
            nosa = request.POST.get('nosa')
            cd = request.POST.get('cd')
            begi_date = request.POST.get('begi_date')
            end_date = request.POST.get('end_date')
            gr = request.POST.get('optradio2')
            gd = request.POST.get('gd')
            awpsfooe = request.POST.get('awpsfooe')
            nossp = request.POST.get('nossp')
            nosmp = request.POST.get('nosmp')
            eraipf = request.POST.get('optradio4')
            proof_file = request.FILES.get('proof_file')
            remarks = request.POST.get('remarks')
            obj3 = events(category=category,eof=eof,topdpo=topdpo,nop=nop,adcc=adcc,session=session,ct=ct,nosa=nosa,cd=cd,begi_date=begi_date,end_date=end_date,gr=gr,gd=gd,awpsfooe=awpsfooe,nossp=nossp,nosmp=nosmp,eraipf=eraipf,proof_file=proof_file,remarks=remarks,email=faculty_instance)
            obj3.save()
        elif pk == 4:
            category = request.POST.get('category')
            noaa = request.POST.get('noaa')
            paf = request.POST.get('paf')
            ao = request.POST.get('ao')
            prize = request.POST.get('prize')
            ad = request.POST.get('award_date')
            remark = request.POST.get('remark')
            proof_file = request.FILES.get('proof_file')
            obj4 = awards_and_achievments(category=category,noaa=noaa,paf=paf,ao=ao,prize=prize,ad=ad,remark=remark,session=session,proof_file=proof_file,email=faculty_instance)
            obj4.save()
        elif pk == 5:
            category = request.POST.get('category')
            nofa = request.POST.get('nofa')
            dop = request.POST.get('dop')
            amount = request.POST.get('amount')
            status = request.POST.get('optradio2')
            proof_file = request.FILES.get('proof_file')
            obj5 = sponsored_research(category=category,nofa=nofa,dop=dop,amount=amount,session=session,status=status,proof_file=proof_file,email=faculty_instance)
            obj5.save()
        elif pk == 6:
            noa = request.POST.get('noa')
            top = request.POST.get('top')
            noj = request.POST.get('noj')
            nop = request.POST.get('nop')
            vi = request.POST.get('vi')
            pn = request.POST.get('pn')
            pd = request.POST.get('begi_date')
            isnp = request.POST.get('isnp')
            isno = request.POST.get('isno')
            level = request.POST.get('optradio3')
            doi = request.POST.get('doi')
            lwj = request.POST.get('lwj')
            lap = request.POST.get('lap')
            lrsj = request.POST.get('lrsj')
            aiop = request.POST.get('aiop')
            ssa = request.POST.get('optradio2')
            details = request.POST.get('details')
            index_by = request.POST.get('optradio1')
            quartile = request.POST.get('optradio')
            proof_file = request.FILES.get('proof_file')
            obj6 = research_journal(noa=noa,top=top,noj=noj,nop=nop,vi=vi,pn=pn,pd=pd,session=session,isnp=isnp,isno=isno,level=level,doi=doi,lwj=lwj,lap=lap,lrsj=lrsj,aiop=aiop,ssa=ssa,details=details,index_by=index_by,quartile=quartile,proof_file=proof_file,email=faculty_instance)
            obj6.save()
        elif pk == 7:
            noa = request.POST.get('noa')
            toc = request.POST.get('toc')
            top = request.POST.get('top')
            topc = request.POST.get('topc')
            level = request.POST.get('optradio3')
            isnp = request.POST.get('isnp')
            nop = request.POST.get('nop')
            pd = request.POST.get('begi_date')
            doi = request.POST.get('doi')
            lwj = request.POST.get('lwj')
            aitp = request.POST.get('aitp')
            ssa = request.POST.get('optradio2')
            details = request.POST.get('details')
            index_by = request.POST.get('optradio1')
            proof_file = request.FILES.get('proof_file')
            obj7 = research_conference(noa=noa,toc=toc,top=top,topc=topc,level=level,isnp=isnp,nop=nop,pd=pd,session=session,doi=doi,lwj=lwj,aitp=aitp,ssa=ssa,details=details,index_by=index_by,proof_file=proof_file,email=faculty_instance)
            obj7.save()
        elif pk == 8:
            noa = request.POST.get('noa')
            tob = request.POST.get('tob')
            top = request.POST.get('top')
            level = request.POST.get('optradio3')
            isbn = request.POST.get('isbn')
            nop = request.POST.get('nop')
            pd = request.POST.get('begi_date')
            doi = request.POST.get('doi')
            lwj = request.POST.get('lwj')
            aitp = request.POST.get('aitp')
            ssa = request.POST.get('optradio2')
            details = request.POST.get('details')
            index_by = request.POST.get('optradio1')
            proof_file = request.FILES.get('proof_file')
            obj8 = research_book(noa=noa,tob=tob,top=top,level=level,isbn=isbn,nop=nop,pd=pd,session=session,doi=doi,lwj=lwj,aitp=aitp,ssa=ssa,details=details,index_by=index_by,proof_file=proof_file,email=faculty_instance)
            obj8.save()
        elif pk == 9:
            sop = request.POST.get('optradio1')
            gi = request.POST.get('nof')
            ag = request.POST.get('ag')
            top = request.POST.get('top')
            gc = request.POST.get('gc')
            pfd = request.POST.get('filed_date')
            pd = request.POST.get('begi_date')
            pg = request.POST.get('optradio2')
            ssa = request.POST.get('optradio')
            details = request.POST.get('details')
            link = request.POST.get('nof')
            proof_file = request.FILES.get('proof_file')
            obj9 = patents(sop=sop,gi=gi, ag=ag, top=top, gc=gc,pfd=pfd, pd=pd, session=session, pg=pg, ssa=ssa, details=details, link=link, proof_file=proof_file,email=faculty_instance)
            obj9.save()
        elif pk == 10:
            nos = request.POST.get('nos')
            ens = request.POST.get('ens')
            urns = request.POST.get('urns')
            eys = request.POST.get('enrollmentyear')
            tod = request.POST.get('tod')
            visor = request.POST.get('optradio2')
            dov = request.POST.get('dov')
            noe = request.POST.get('noe')
            obj10 = guided(nos=nos, ens=ens, urns=urns, eys=eys, tod=tod, visor=visor, dov=dov, noe=noe, session=session,email=faculty_instance)
            obj10.save()
        elif pk == 11:
            category = request.POST.get('category')
            toe = request.POST.get('toe')
            sa = request.POST.get('sa')
            doe = request.POST.get('doe')
            rpt = request.POST.get('optradio2')
            begi_date = request.POST.get('begi_date')
            end_date = request.POST.get('end_date')
            venue = request.POST.get('venue')
            proof_file = request.FILES.get('proof_file')
            obj11 = resource(category=category,toe=toe, sa=sa,doe=doe, rpt=rpt, begi_date=begi_date, end_date=end_date, session=session, venue=venue, proof_file=proof_file,email = faculty_instance)
            obj11.save()
        elif pk == 13:
            faculty_instance.name = request.POST.get('name')
            faculty_instance.contact_number = request.POST.get('mobile_no')
            faculty_instance.email = request.POST.get('email')
            faculty_instance.gender = request.POST.get('optradio')
            faculty_instance.department = request.POST.get('department')
            faculty_instance.emp_id = request.POST.get('emp_id')
            faculty_instance.designation = request.POST.get('designation')
            faculty_instance.aos = request.POST.get('aos')
            faculty_instance.hq = request.POST.get('highest_qualification')
            faculty_instance.univ_name = request.POST.get('univ_name')
            faculty_instance.pshd = request.POST.get('pshd')
            faculty_instance.pan_no = request.POST.get('pan_no')
            faculty_instance.dob = request.POST.get('dob')
            faculty_instance.jd = request.POST.get('jd')
            pd = request.POST.get('pd')
            if pd == '':
                faculty_instance.pd = None
            faculty_instance.address = request.POST.get('address')
            if request.FILES.get('profile_picture'):
                faculty_instance.profile_picture = request.FILES.get('profile_picture')
            if request.FILES.get('jr'):
                faculty_instance.jr = request.FILES.get('jr')
            if request.FILES.get('ol'):
                faculty_instance.of = request.FILES.get('ol')
            if request.FILES.get('hdc'):
                faculty_instance.hdc = request.FILES.get('hdc')
            if request.FILES.get('ss'):
                faculty_instance.ss = request.FILES.get('ss')
            if request.FILES.get('awards'):
                faculty_instance.certificate = request.FILES.get('awards')
            faculty_instance.phd_univ = request.POST.get('phd_univ')
            phd_dor = request.POST.get('phd_dor')
            if phd_dor == '':
                faculty_instance.phd_dor = None
            faculty_instance.norp = request.POST.get('norp')
            faculty_instance.save()
        elif pk == 14:
            faculty_instance = Faculty.objects.get(email=request.POST.get('existing_email'))
            faculty_instance.name = request.POST.get('updated_name')
            faculty_instance.contact_number = request.POST.get('updated_number')
            if request.POST.get('updated_email').endswith('@skit.ac.in'):
                faculty_instance.email = request.POST.get('updated_email')
            else:
                messages.error(request,'Mail should always end with @skit.ac.in')
                return redirect(reverse('directory'))
            faculty_instance.department = request.POST.get('updated_department')
            faculty_instance.emp_id = request.POST.get('updated_id')
            faculty_instance.status = request.POST.get('updated_status')
            faculty_instance.save()
            return redirect(reverse('directory'))
        elif pk == 15:
            emp_id = request.POST.get('emp_id')
            emp_name = request.POST.get('name_per')
            if request.POST.get('new_email').strip().endswith('@skit.ac.in'):
                email = request.POST.get('new_email').strip()
            else:
                messages.error(request, 'Mail should always end with @skit.ac.in')
                return redirect(reverse('directory'))
            department = request.POST.get('selected_department')
            con_no = request.POST.get('contact_number')
            status = request.POST.get('selected_status')
            obj12 = Faculty(name=emp_name,emp_id=emp_id,email=email,department=department,contact_number=con_no,status=status)
            obj12.save()
            return redirect(reverse('directory'))
        return redirect(reverse('success'))
    return render(request, 'about')

@session_login_required
def edit_profile(request):
    faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))
    context = {'key': faculty_instance}
    return render(request,'editProfile.html',context=context)

def successfulsubmission(request):
    return render(request,'submitSuccess.html')


def upload_excel(request, pk):
    if request.method == 'POST':
        dataset = Dataset()
        new_data = request.FILES['excel_file']
        if not new_data or new_data.name == '':
            return "No file selected or invalid file", 400
        imported_data = dataset.load(new_data.read(), format='xlsx')
        df = pd.DataFrame(
            imported_data.dict,
            columns=imported_data.headers
        )
        if pk == 0:

            for data in imported_data.dict:
                value = Student_Directory(name=data['name'],roll_no=data['roll_no'],college_id=data['college_id'],email=data['email_id'],student_phone_no=data['student_phone_no'],parent_phone_no=data['parent_phone_no'],address=data['address'])
                value.save()

            # messages.success(request,'We are glad to share that your excel file is uploaded successfully!')
            return redirect(reverse('student-directory'))

        elif pk == 1:
            df.columns = df.columns.str.lower().str.replace(' ', '_').str.strip()
            for data in df.to_dict(orient='records'):
                if not data['name']:
                    continue

                value = Faculty(name=data['name'],emp_id=data['employee_id'],email=data['email'],department=data['department'],contact_number=data['contact_number'],status="NR")
                value.save()

            return redirect(reverse('directory'))

    return render(request,'about.html')

def deleteuser(request):
    if request.method == "POST":

        faculty_id = request.POST.get('faculty_emp_id')
        faculty_object = get_object_or_404(Faculty, emp_id=faculty_id)
        faculty_object.delete()

    return redirect(reverse('directory'))

@session_login_required
def all_forms(request,pk):
    value = request.session.get('topLeftBar')
    if value == 'ad' or value == 'spa' or value == 'fa':
        data = Faculty.objects.get(pk=request.session.get('user_id'))
    elif value == 'student':
        data = Student_Directory.objects.get(pk=request.session.get('user_id'))
    else:
        data = None
    form_number = pk
    secret_key = data
    return render(request,'forms.html',{'form_number': form_number, 'value': secret_key})

@session_login_required
def fdp(request):
    forms = [
        {'no': '0', 'form': "Non-teaching Staff Profile Details"},
        {'no': '1', 'form': "Faculty Participation"},
        {'no': '2', 'form': "MOOC's/Short Term Course/Course Completion"},
        {'no': '3', 'form': "Events Organized by Department"},
        {'no': '4', 'form': "Faculty Awards and Achievements"},
        {'no': '5', 'form': "Sponsored Research/Grant Received/Consultancy"},
        {'no': '6', 'form': "Research Publication - Journals"},
        {'no': '7', 'form': "Research Publication - Conference Publication"},
        {'no': '8', 'form': "Research Publication - Book and Book Chapters"},
        {'no': '9', 'form': "Patents"},
        {'no': '10', 'form': "M.Tech/Ph.D Guided"},
        {'no': '11', 'form': "Resource Person"}
    ]
    return render(request, 'fdp_forms.html',context={'values': forms})

@session_login_required
def custom_logout(request):
    if 'user_id' in request.session and 'topLeftBar' in request.session:
        del request.session['user_id']
        del request.session['topLeftBar']
        return redirect(reverse('home'))
    return redirect(reverse('about'))

# Create your views here.

def index(request):
    return render(request,'index.html')

def student(request):
    stu_dir_instance = Student_Directory.objects.values('batch').annotate(
        count=Count('id')
    ).order_by('batch')
    context = {'dir_ins':stu_dir_instance}
    return render(request, 'student_card_details.html',context = context)

def faculty(request):
    fac_dir_instance = Faculty.objects.values('department').annotate(
        count=Count('id')
    ).order_by('department')
    for item in fac_dir_instance:
        print("Department send from faculty is: ",item['department'])
    context = {'dir_ins':fac_dir_instance}
    return render(request, 'faculty_card_details.html',context = context)

@session_login_required
def profile(request):
    if 'user_id' in request.session and 'topLeftBar' in request.session:
        try:
            modal = request.session.get('topLeftBar')
            if modal == 'ad' or modal == 'spa' or modal == 'fa':
                user = Faculty
            else:
                user = Student_Directory
        except:
            user = None
    value = user.objects.get(pk=request.session.get('user_id'))

    context = {'data': value}
    return render(request,'profile.html', context=context)


@session_login_required
def student_directory(request):
    stu_data = Student_Directory.objects.all()
    context = {'stu_data': stu_data}
    return render(request,'student_directory.html',context = context)

def about(request):
    return render(request,'about.html')

@session_login_required
def stu_card_details(request,pk):
    batches = Student_Directory.objects.filter(batch = pk)
    context = {'stu_data': batches }
    return render(request,'batch_details.html',context=context)

@session_login_required
def fac_card_details(request,pk):
    print("Value receieved in card details is: ",pk)
    department = Faculty.objects.filter(department = pk)
    context = {'fac_data': department }
    return render(request,'faculty_details.html',context=context)

def login_page(request):
    return render(request,'login.html')

@session_login_required
def progress(request):
    email = Faculty.objects.get(pk=request.session.get('user_id'))
    no_of_awards = list(awards_and_achievments.objects.filter(email=email).values('category').annotate(count=Count('id')))
    label_map = {choice.value: choice.label for choice in cat}

    for item in no_of_awards:
        item['category_display'] = label_map.get(item['category'], item['category'])

    events_instance = list(events.objects.filter(email=email).values('category').annotate(count=Count('id')))
    for item in events_instance:
        item['category_display'] = label_map.get(item['category'], item['category'])

    faculty_participartion_data = list(Faculty_participation_data.objects.filter(email=email).values('category').annotate(count=Count('id')))
    for item in faculty_participartion_data:
        item['category_display'] = label_map.get(item['category'], item['category'])

    guided_instance = guided.objects.filter(email=email).count()
    mooc_course_instance = list(mooc_course.objects.filter(email=email).values('category').annotate(count=Count('id')))
    for item in mooc_course_instance:
        item['category_display'] = label_map.get(item['category'], item['category'])

    patents_instance = patents.objects.filter(email=email).count()
    research_book_instance = research_book.objects.filter(email=email).count()
    research_conference_instance = research_conference.objects.filter(email=email).count()
    research_journal_instance = research_journal.objects.filter(email=email).count()
    resource_instance = resource.objects.filter(email=email).count()
    sponsored_research_instance = list(sponsored_research.objects.filter(email=email).values('category').annotate(count=Count('id')))
    for item in sponsored_research_instance:
        item['category_display'] = label_map.get(item['category'], item['category'])

    total_forms = sum(item['count'] for item in no_of_awards) + sum(item['count'] for item in events_instance) + sum(item['count'] for item in faculty_participartion_data) + guided_instance + sum(item['count'] for item in mooc_course_instance) + patents_instance + research_book_instance + research_conference_instance + research_journal_instance + resource_instance + sum(item['count'] for item in sponsored_research_instance)
    total_remaining_field_forms = 33 - (len(no_of_awards) + len(events_instance) + len(faculty_participartion_data) + (1 if guided_instance > 0 else 0) + len(mooc_course_instance) + (1 if patents_instance > 0 else 0) + (1 if research_book_instance > 0 else 0) + (1 if research_conference_instance > 0 else 0) + (1 if research_journal_instance > 0 else 0) + (1 if resource_instance > 0 else 0) + len(sponsored_research_instance))
    context = {'total_forms': total_forms,'total_rff' : total_remaining_field_forms, 'faa1': no_of_awards, 'eod1': events_instance, 'fdp1': faculty_participartion_data, 'mp1': guided_instance, 'msc1' : mooc_course_instance, 'patents1': patents_instance, 'rpb1': research_book_instance, 'rpcp1': research_conference_instance, 'rpj1': research_journal_instance, 'rp1': resource_instance, 'sgc1': sponsored_research_instance}
    return render(request,'progresschart.html',context)

@session_login_required
def directory(request):
    if 'user_id' in request.session and 'topLeftBar' in request.session:
        try:
            modal = request.session.get('topLeftBar')
            if modal == 'ad' or modal == 'spa' or modal == 'fa':

                value = Faculty.objects.all()

                context = { 'data': value }
                return render(request,'directory.html',context=context)
            else:
                return render(request,'about.html')
        except:
            user = None
    return None

@session_login_required
def faculty_report(request):
    registerd_faculties = Faculty.objects.filter(status="R")
    context = {'rf' : registerd_faculties}
    return render(request,'faculty_report.html',context)

@session_login_required
def download(request):
    if request.method == "POST":
        if request.POST.get('file_type') == 'excel':
            CHOICES_FIELDS = ['department', 'designation', 'aos', 'hq', 'status', 'role', 'gender']
            files_field = ['profile_picture', 'jr', 'of', 'hdc', 'ss', 'certificate']
            values = request.POST.getlist('optcheck[]')
            result_instance = Faculty.objects.filter(department__in=values,status="R")

            data = []

            # 2. Iterate and process each instance
            for result in result_instance:

                row_dict = model_to_dict(result)

                # b) Dynamically override the code value with the display value
                for field_name in CHOICES_FIELDS:
                    # getattr to call the correct get_FIELDNAME_display() method

                    display_method = getattr(result, f'get_{field_name}_display')

                    row_dict[field_name] = display_method()

                for field in files_field:
                    hyperlink_text = "https://uttkarsh007.pythonanywhere.com/media/" + str(row_dict[field])
                    hyperlink_formula = f'=HYPERLINK("{hyperlink_text}", "View File online")'
                    row_dict[field] = hyperlink_formula

                data.append(row_dict)

            df = pd.DataFrame(data)
            #For CSV
            json_data = df.to_json(orient='records', date_format='iso')
            request.session['csv_data'] = json_data
            #For Excel
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer,index = False,sheet_name="faculty_report",header=['S.No.','Name','Contact Number','Email','Department','Gender','Address','Employee ID','Role','Status','Desigantion','Area of Specialization','Highest Qualification','University Name(highest degree)','Passing Year of Highest Degree','PAN NO.','Date of birth','Joining Data','Promotion Date','Profile Picture(Link)','Joining Report','Offer Letter','Salary Slip','Highest Degree Certificate','Extra Certificate','PHD pursuing University Name','PHD Date of Registration','Number of research paper'])

            writer.close()
            excel_data = base64.b64encode(output.getvalue())
            request.session['excel_data'] = excel_data.decode('utf-8')


    elif request.method == "GET":
        if request.GET.get('file_type') == 'excel_repo':
            excel_data = request.session.get('excel_data').encode('utf-8')
            retrieved_excel_data = base64.b64decode(excel_data)
            response = HttpResponse(
                retrieved_excel_data,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="faculty_report.xlsx"'
            return response

        elif request.GET.get('file_type') == 'excel_dir':
            result_instance = Faculty.objects.all()

            data = [
                {
                    'Name': result.name,
                    'Email': result.email,
                    'Employee ID': result.emp_id,
                    'Department': result.get_department_display(),
                    'Contact Number': result.contact_number,
                    'Status': result.get_status_display()
                }
                for result in result_instance
            ]

            df = pd.DataFrame(data)
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='openpyxl')
            df.to_excel(writer, index=False, sheet_name="faculty_directory")
            writer.close()
            excel_data = output.getvalue()
            response = HttpResponse(
                excel_data,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="faculty_directory.xlsx"'
            return response

        elif request.GET.get('file_type') == 'excel_stu_dir':
            result_instance = Student_Directory.objects.all()
            data = [
                {
                    'Name': result.name,
                    'Roll No': result.roll_no,
                    'College ID': result.college_id,
                    'Email': result.email,
                    'Student Phone No': result.student_phone_no,
                    'Parent Phone No': result.parent_phone_no,
                    'Address': result.address
                }
                for result in result_instance
            ]

            df = pd.DataFrame(data)
            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='openpyxl')
            df.to_excel(writer, index=False, sheet_name="student_directory")
            writer.close()
            excel_data = output.getvalue()
            response = HttpResponse(
                excel_data,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="student_directory.xlsx"'
            return response

        elif request.GET.get('file_type') == 'csv_repo' or request.GET.get('file_type') == 'csv_dir' or request.GET.get('file_type') == 'csv_stu_dir':
            return render(request,'page_under_construction.html')

    return redirect(reverse('about'))
