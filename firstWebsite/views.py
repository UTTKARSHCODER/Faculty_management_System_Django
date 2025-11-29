from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from tablib import Dataset

from MyFirstDjangoWebsite import settings
from firstWebsite.modals import Contact, Faculty, Faculty_participation_data, mooc_course, events, \
    awards_and_achievments, sponsored_research, research_journal, research_conference, research_book, patents, guided, \
    resource, non_teaching_staff, designation
from .modals import Student_Directory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from .resources import StudentResources

batches = [
    {'batch':'3CS-A','no_of_stu':'64'},
    {'batch':'3CS-B','no_of_stu':'56'},
    {'batch':'3CS-C','no_of_stu':'60'},
    {'batch':'3CS-D','no_of_stu':'62'},
    {'batch':'3CS-E','no_of_stu':'63'},
    {'batch':'3CS-F','no_of_stu':'58'},
    {'batch':'3CS(AI)-A','no_of_stu':'63'},
    {'batch':'3CS(AI)-B','no_of_stu':'51'},
    {'batch':'3CS(DS)-A','no_of_stu':'48'},
    {'batch':'3CS(IOT)-A','no_of_stu':'24'},
    {'batch':'3CS(IOT)-B','no_of_stu':'18'}
]

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

            adapter = GoogleOAuth2Adapter(request)
            try:
                if email.endswith('@skit.ac.in'):
                    if users_post == 'spa' or users_post == 'ad' or users_post == 'fa':
                        User = Faculty
                        user = User.objects.get(email=email,role__iexact=users_post)
                    elif users_post == 'student':
                        User = Student_Directory
                        user = User.objects.get(email=email)
                    else:
                        User = None
                        user = None
                    # If login is successful:
                    request.session["secret_key"] = user.email
                    request.session['topLeftBar'] = users_post
                    return JsonResponse({
                        'success': True,
                        'redirect_url': '/profile'  # Redirect to the home or dashboard page
                    })
                else:
                    error_message = f"Access denied: The email '{email}' is not authorized to log in."

                    # You can optionally add a Django message for standard page rendering
                    messages.error(request, error_message)

                    return JsonResponse({
                        'success': False,
                        'error': error_message
                    }, status=403)
            except User.DoesNotExist:

                error_message = f"Access denied: The email '{email}' is not authorized to log in."

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

def save_all_forms(request, pk):
    if request.method == 'POST':
        session = request.POST.get('sessionyear')
        faculty_instance = Faculty.objects.get(email=request.session.get('secret_key'))
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
            obj2 = mooc_course(timeline=timeline,noc=noc,doc=doc,begi_date=begi_date,end_date=end_date,offer=offer,ctype=ctype,topper_in=topper_in,session=session,remarks=remarks,proof_file=proof_file,email=faculty_instance)
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
            faculty_instance.jr = request.FILES.get('jr')
            faculty_instance.of = request.FILES.get('ol')
            faculty_instance.hdc = request.FILES.get('hdc')
            faculty_instance.ss = request.FILES.get('ss')
            faculty_instance.certificate = request.FILES.get('awards')
            faculty_instance.phd_univ = request.POST.get('phd_univ')
            phd_dor = request.POST.get('phd_dor')
            if phd_dor == '':
                faculty_instance.phd_dor = None
            faculty_instance.norp = request.POST.get('norp')
            faculty_instance.save()
        return redirect(reverse('success'))
    return render(request, 'about')

def edit_profile(request):
    faculty_instance = Faculty.objects.get(email=request.session.get('secret_key'))
    context = {'key': faculty_instance}
    return render(request,'editProfile.html',context=context)

def successfulsubmission(request):
    return render(request,'submitSuccess.html')


def upload_excel(request):
    if request.method == 'POST':
        student_resource = StudentResources()
        dataset = Dataset()
        new_students = request.FILES['excel_file']
        imported_data = dataset.load(new_students.read(), format = 'xlsx')
        for data in imported_data:
            value = Student_Directory(*data)

        value.save()
        # messages.success(request,'We are glad to share that your excel file is uploaded successfully!')
        return render(request,'student_directory.html')
    return render(request,'about.html')

def all_forms(request,pk):
    value = request.session.get('topLeftBar')
    if value == 'ad' or value == 'spa' or value == 'fa':
        data = Faculty.objects.get(email=request.session.get('secret_key'))
    elif value == 'student':
        data = Student_Directory.objects.get(email=request.session.get('secret_key'))
    else:
        data = None
    form_number = pk
    secret_key = data
    return render(request,'forms.html',{'form_number': form_number, 'value': secret_key})

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

def custom_logout(request):
    if 'secret_key' in request.session and 'topLeftBar' in request.session:
        del request.session['secret_key']
        del request.session['topLeftBar']
        return redirect(reverse('home'))
    return redirect(reverse('about'))

stu_data = Student_Directory.objects.all()
# Create your views here.
def index(request):
    context = {'batches':batches}
    return render(request, 'index.html',context = context)

def profile(request):
    if 'secret_key' in request.session and 'topLeftBar' in request.session:
        try:
            modal = request.session.get('topLeftBar')
            if modal == 'ad' or modal == 'spa' or modal == 'fa':
                user = Faculty
            else:
                user = Student_Directory
        except:
            user = None
    value = user.objects.get(email = request.session.get('secret_key'))
    #Setting department complete value
    if value.department == "CSE":
        department = "Computer Science and Engineering"
    elif value.department == "CSE(AI)":
        department = "Computer Science and Engineering(AI)"
    elif value.department == "CSE(DS)":
        department = "Computer Science and Engineering(DS)"
    elif value.department == "CSE(IOT)":
        department = "Computer Science and Engineering(IOT)"
    else:
        department = "Not Selected"
    # Setting designation complete value
    if value.designation == "AP1":
        designation1 = "Assistant Professor 1"
    elif value.desigantion == "AP2":
        designation1 = "Assistant Professor 2"
    elif value.desigantion == "ASP1":
        designation1 = "Associate Professor 1"
    elif value.desigantion == "ASP2":
        designation1 = "Associate Professor 2"
    elif value.desigantion == "P":
        designation1 = "Professor"
    else:
        designation1 = None

    context = {'data': value, 'department': department,'designation': designation1}
    return render(request,'profile.html', context=context)

def allocated_batches(request):
    context = {'card_data': stu_data}
    return render(request,'allocated_batches.html',context= context)

def student_directory(request):
    stu_data = Student_Directory.objects.all()
    context = {'stu_data': stu_data}
    return render(request,'student_directory.html',context = context)

def about(request):
    return render(request,'about.html')

def stu_card_details(request,pk):
    batch = Student_Directory.objects.filter(batch = pk)
    context = {'stu_data': batch}
    return render(request,'batch_details.html',context=context)

def login_page(request):
    return render(request,'login.html')

def progress(request):
    return render(request,'progress.html')

def contact(request):
    if request.method == "POST":
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        feedback = request.POST.get('feedback')
        contact = Contact(first_name = first_name, last_name = last_name, email = email, feedback = feedback)
        contact.save()
    return HttpResponse("This is contact page")