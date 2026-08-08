import uuid
from datetime import datetime

from django.http.response import JsonResponse
from django.utils import timezone
import re
import firstWebsite.validations as va
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse

from MyFirstDjangoWebsite import settings
from firstWebsite.modals import Faculty, non_teaching_staff, Faculty_participation_data, mooc_course, events, \
    awards_and_achievments, sponsored_research, research_journal, research_conference, research_book, patents, guided, \
    resource
from firstWebsite.validations import nameValidate, radiocheck
from firstWebsite.views import session_login_required
import jwt

@session_login_required
def save_all_forms(request, form_no):
    if form_no:
        if request.method == 'POST':

            session = request.POST.get('sessionyear')
            faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))

            if form_no == 16:
                # Profile Picture input can also be added on later discussion
                name = request.POST.get('name').strip()
                if not va.nameValidate(request,name,"Name"):
                    return redirect('all_forms',pk=form_no)

                mobile_no = request.POST.get('mobile_no').strip()
                if not va.mobileNumberValidate(request,mobile_no):
                    return redirect('all_forms',pk=form_no)

                department = request.POST.get('department',"").strip()

                lab_no = request.POST.get('lab_no').strip()
                if not va.nameValidate(request,lab_no,"Lab Number"):
                    return redirect('all_forms', form_no=form_no)

                designation = request.POST.get('designation').strip()
                if not va.nameValidate(request,designation,"Designation"):
                    return redirect('all_forms', form_no=form_no)

                emp_id = int(request.POST.get('emp_id') or 0)
                if not va.numberValidate(request, emp_id, "Employee ID"):
                    return redirect('all_forms', form_no=form_no)

                highest_qual = request.POST.get('highest_qualification').strip()
                if not va.nameValidate(request,highest_qual,"Highest Qualification"):
                    return redirect('all_forms', form_no=form_no)

                university_name = request.POST.get('univ_name').strip()
                if not va.nameValidate(request,university_name,"University Name"):
                    return redirect('all_forms', form_no=form_no)

                pshd = int(request.POST.get('pshd') or 0)
                if not va.numberValidate(request,pshd,"Passing Year of Highest Degree"):
                    return redirect('all_forms', form_no=form_no)

                professional_course = request.POST.getlist('professional_courses')
                if not va.radiocheck(request,professional_course,"Professional Course"):
                    return redirect('all_forms',pk=form_no)

                pan_no = request.POST.get('pan_no').strip()
                if not va.validate_pan(pan_no) or not pan_no:
                    messages.error(request, "Please enter a valid PAN number")
                    return redirect('all_forms', form_no=form_no)

                dob = request.POST.get('dob')
                try:
                    selected_date = datetime.strptime(dob,'%Y-%m-%d').date()

                    max_date = datetime.strptime('2001-12-31', '%Y-%m-%d').date()
                    min_date = datetime.strptime('1930-01-01','%Y-%m-%d').date()

                    if not min_date < selected_date < max_date:
                        messages.error(request,f"Please select/enter date of birth in range of 1930-01-01 to 2001-12-31.You selected {selected_date}")
                        return redirect('all_forms',pk=form_no)

                except(ValueError, TypeError):
                    messages.error(request,"Please select/enter a valid date of birth.")
                    return redirect('all_forms', form_no=form_no)

                joining_date = request.POST.get('jd')
                try:
                    selected_date = datetime.strptime(joining_date,'%Y-%m-%d').date()

                    min_date = datetime.strptime('2000-01-01','%Y-%m-%d').date()

                    if selected_date < min_date:
                        messages.error(request,"Please select/enter date greater than 2000-01-01")
                        return redirect('all_forms',pk=form_no)

                except(ValueError, TypeError):
                    messages.error(request,"Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                promotion_date = request.POST.get('pd')
                if promotion_date == '':
                    promotion_date = None

                if request.FILES.get('jr'):
                    joining_report = request.FILES['jr']
                    if not va.fileValidate(request,joining_report,"Joining Report"):
                        return redirect('all_forms', form_no=form_no)
                else:
                    messages.error(request,"No file selected for joining report. Please select one!")
                    return redirect('all_forms',pk=form_no)

                if request.FILES.get('ol'):
                    offer_letter = request.FILES['jr']
                    if not va.fileValidate(request,offer_letter,"Offer Letter"):
                        return redirect('all_forms', form_no=form_no)
                else:
                    messages.error(request,"No file selected for joining report. Please select one!")
                    return redirect('all_forms',pk=form_no)

                if request.FILES.get('hdc'):
                    higher_degree_certificate = request.FILES['hdc']
                    if not va.fileValidate(request,higher_degree_certificate,"Higher Degree Certificate"):
                        return redirect('all_forms', form_no=form_no)
                else:
                    messages.error(request,"No file selected for joining report. Please select one!")
                    return redirect('all_forms',pk=form_no)

                if request.FILES.get('ss'):
                    salary_slip = request.FILES['ss']
                    if not va.fileValidate(request,salary_slip,"Salary Slip"):
                        return redirect('all_forms', form_no=form_no)
                else:
                    salary_slip = None

                if request.FILES.get('awards'):
                    certificate = request.FILES['awards']
                    if not va.fileValidate(request,certificate,"Co-curricular Certificate"):
                        return redirect('all_forms', form_no=form_no)
                else:
                    certificate = None

                obj = non_teaching_staff(session=session, name=name, mobile_no=mobile_no, email=faculty_instance, department=department, Lab_no=lab_no, designation=designation, emp_id=emp_id, highest_qual=highest_qual, university_name=university_name, pshd=pshd, professional_course=professional_course, pan_no=pan_no,dob=dob, joining_date=joining_date, promotion_date=promotion_date, joining_report=joining_report, offer_letter=offer_letter, higher_degree_certificate=higher_degree_certificate, salary_slip=salary_slip, certificate=certificate)
                obj.save()
                messages.success(request, 'Form filled successfully!')
                return redirect(reverse('fdp'))

            elif form_no == 1:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms', form_no=form_no)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request,top,"Title of program"):
                    return redirect('all_forms', form_no=form_no)

                mode = request.POST.get('optradio').strip()
                if not va.radiocheck(request,mode,"mode"):
                    return redirect('all_forms', form_no=form_no)

                level = request.POST.get('optradio1').strip()
                if not va.radiocheck(request,level,"level"):
                    return redirect('all_forms', form_no=form_no)

                organizer = request.POST.get('organizer').strip()
                if not va.nameValidate(request,organizer,"Organizer"):
                    return redirect('all_forms', form_no=form_no)

                sponser = request.POST.get('sponser').strip()
                if not va.nameValidate(request,sponser,"Sponser"):
                    return redirect('all_forms', form_no=form_no)

                approval = request.POST.get('optradio2').strip()
                if not va.radiocheck(request,approval,"(SKIT approved)"):
                    return redirect('all_forms', form_no=form_no)

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)
                    begi_date = selected_date

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)
                    end_date = selected_date

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                num_of_days = (end_date - begi_date).days

                proof_approval = request.POST.get('optradio3').strip()
                if not va.radiocheck(request,proof_approval,"Proof Approval"):
                    return redirect('all_forms',pk=form_no)

                if request.FILES.get('proof_file'):
                    proof_file_path = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file_path,"Proof File"):
                        return redirect('all_forms', form_no=form_no)

                obj1 = Faculty_participation_data(category=category,top=top,mode=mode,level=level,organizer=organizer,sponsors=sponser,approval=approval,begi_date=begi_date,end_date=end_date,session=session,no_of_days=num_of_days,proof_enclosed=proof_approval,proof_file=proof_file_path,email=faculty_instance)
                obj1.save()

            elif form_no == 2:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=form_no)

                timeline = request.POST.get('toc').strip()
                if not va.nameValidate(request,category,"Timeline of Course"):
                    return redirect('all_forms',pk=form_no)

                noc = request.POST.get('noc').strip()
                if not va.nameValidate(request,category,"Name of Course"):
                    return redirect('all_forms',pk=form_no)

                doc = request.POST.get('optradio3').strip()
                if not va.nameValidate(request,category,"Duration of Course"):
                    return redirect('all_forms',pk=form_no)

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                offer = request.POST.get('ofo').strip()
                if not va.nameValidate(request, category, "Offering Agency/ Organizer"):
                    return redirect('all_forms', form_no=form_no)

                ctype = request.POST.get('optradio1').strip()
                if not va.radiocheck(request, category, "Certificate Type"):
                    return redirect('all_forms', form_no=form_no)

                topper_in = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, category, "Topper Category"):
                    return redirect('all_forms', form_no=form_no)

                remarks = request.POST.get('remarks').strip()

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file,"Proof File"):
                        return redirect('all_forms',pk=form_no)

                obj2 = mooc_course(category=category,timeline=timeline,noc=noc,doc=doc,begi_date=begi_date,end_date=end_date,offer=offer,ctype=ctype,topper_in=topper_in,session=session,remarks=remarks,proof_file=proof_file,email=faculty_instance)
                obj2.save()

            elif form_no == 3:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=form_no)

                eof = request.POST.getlist('optradio3')
                if not va.radiocheck(request,eof,"Event organized for"):
                    return redirect('all_forms',pk=form_no)

                nofc = request.POST.get('nofc').strip()
                if not va.nameValidate(request,nofc,"Name of Faculty Coordinator(s)"):
                    return redirect('all_forms',pk=form_no)

                topdpo = request.POST.get('topdpo').strip()
                if not va.nameValidate(request,topdpo,"Title of Professional Development Program Organized"):
                    return redirect('all_forms',pk=form_no)

                nop = int(request.POST.get('nop') or 0)
                if not va.numberValidate(request,nop,"Number of participants"):
                    return redirect('all_forms',pk=form_no)

                adcc = request.POST.get('adcc').strip()
                if not va.nameValidate(request,adcc,"Academic Department"):
                    return redirect('all_forms',pk=form_no)

                ct = request.POST.get('optradio1').strip()
                if not va.radiocheck(request,ct,"Certificate Type"):
                    return redirect('all_forms',pk=form_no)

                nosa = request.POST.get('nosa').strip()
                if not va.nameValidate(request,nosa,"Name of Sponsoring Agency"):
                    return redirect('all_forms',pk=form_no)

                cd = request.POST.get('cd').strip()
                if not va.nameValidate(request,cd,"Collaboration Details"):
                    return redirect('all_forms',pk=form_no)

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                gr = request.POST.get('optradio2').strip()
                if not va.radiocheck(request,gr,"Grant Recieved"):
                    return redirect('all_forms',pk=form_no)

                gd = request.POST.get('gd').strip()
                if not va.nameValidate(request,gd,"Grant Details"):
                    return redirect('all_forms',pk=form_no)

                acutal_expense = request.POST.get('actual_expenditure').strip()
                if not va.nameValidate(request, acutal_expense, "Actual Expenditure"):
                    return redirect('all_forms',pk=form_no)

                awpsfooe = request.POST.get('awpsfooe').strip()
                if not va.nameValidate(request,gr,"Association with professional societies for organization of event"):
                    return redirect('all_forms',pk=form_no)

                nossp = request.POST.get('nossp').strip()
                if not va.nameValidate(request,gr,"Number of SKIT students participated"):
                    return redirect('all_forms',pk=form_no)

                nosmp = request.POST.get('nosmp').strip()
                if not va.nameValidate(request,nosmp,"Number of staff member participated"):
                    return redirect('all_forms',pk=form_no)

                mapped_sdg = request.POST.getlist('optradio4')
                if not va.radiocheck(request,mapped_sdg, "Mapped SDG"):
                    return redirect('all_forms',pk=form_no)

                eraipf = request.POST.get('optradio5').strip()
                if not va.radiocheck(request,eraipf,"Event Report attached(Yes/No)"):
                    return redirect('all_fomrs',pk=form_no)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file,"Proof file"):
                        return redirect('all_forms',pk=form_no)

                remarks = request.POST.get('remarks')

                obj3 = events(category=category,eof=eof,nofc=nofc,topdpo=topdpo,nop=nop,adcc=adcc,session=session,ct=ct,nosa=nosa,cd=cd,begi_date=begi_date,end_date=end_date,gr=gr,gd=gd,actual_expenditure=acutal_expense,awpsfooe=awpsfooe,nossp=nossp,nosmp=nosmp,map_sdg=mapped_sdg,eraipf=eraipf,proof_file=proof_file,remarks=remarks,email=faculty_instance)
                obj3.save()

            elif form_no == 4:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=form_no)

                noaa = request.POST.get('noaa').strip()
                if not va.nameValidate(request,noaa,"Name of award/Achievement"):
                    return redirect('all_forms',pk=form_no)

                paf = request.POST.get('paf').strip()
                if not va.nameValidate(request, noaa, "Position / Award For"):
                    return redirect('all_forms', form_no=form_no)

                ao = request.POST.get('ao').strip()
                if not va.nameValidate(request, noaa, "Agency / Organization"):
                    return redirect('all_forms', form_no=form_no)

                prize = request.POST.get('prize').strip()
                if not va.nameValidate(request, noaa, "Prize"):
                    return redirect('all_forms', form_no=form_no)

                ad = request.POST.get('award_date')
                try:
                    selected_date = datetime.strptime(ad, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                remark = request.POST.get('remark').strip()

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file,"Proof File"):
                        return redirect('all_forms',pk=form_no)

                obj4 = awards_and_achievments(category=category,noaa=noaa,paf=paf,ao=ao,prize=prize,ad=ad,remark=remark,session=session,proof_file=proof_file,email=faculty_instance)
                obj4.save()

            elif form_no == 5:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=form_no)

                nofa = request.POST.get('nofa').strip()
                if not va.nameValidate(request, nofa, "Name of Funding Agency"):
                    return redirect('all_forms', form_no=form_no)

                dop = int(request.POST.get('dop') or 0)
                if not va.numberValidate(request,dop,"Duration of project"):
                    return redirect('all_forms',pk=form_no)

                amount = int(request.POST.get('amount') or 0)
                if not va.numberValidate(request,amount,"Amount"):
                    return redirect('all_forms',pk=form_no)

                status = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, status, "Status"):
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file,"Proof File"):
                        return redirect('all_forms',pk=form_no)

                obj5 = sponsored_research(category=category,nofa=nofa,dop=dop,amount=amount,session=session,status=status,proof_file=proof_file,email=faculty_instance)
                obj5.save()

            elif form_no == 6:
                noa = request.POST.get('noa').strip()
                if not va.nameValidate(request,noa,"Name of the author(s)"):
                    return redirect('all_forms',pk=form_no)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request,top,"Title of paper"):
                    return redirect('all_forms',pk=form_no)

                noj = request.POST.get('noj').strip()
                if not va.nameValidate(request,noj,"Name of Journal"):
                    return redirect('all_forms',pk=form_no)

                nop = request.POST.get('nop').strip()
                if not va.nameValidate(request,nop,"Name of the Publisher"):
                    return redirect('all_forms',pk=form_no)

                vi = request.POST.get('vi').strip()
                if not va.nameValidate(request,vi,"Volumne, Issue"):
                    return redirect('all_forms',pk=form_no)

                pn = request.POST.get('pn').strip()
                if not va.nameValidate(request,pn,"Page Number"):
                    return redirect('all_forms',pk=form_no)

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                isnp = request.POST.get('isnp').strip()
                if not va.nameValidate(request, isnp, "ISSN number : Print"):
                    return redirect('all_forms', form_no=form_no)

                isno = request.POST.get('isno').strip()
                if not va.nameValidate(request, isno, "ISSN number : Online"):
                    return redirect('all_forms', form_no=form_no)

                level = request.POST.get('optradio3').strip()
                if not va.nameValidate(request, level, "Level (National/ International)"):
                    return redirect('all_forms', form_no=form_no)

                doi = request.POST.get('doi').strip()
                if not va.nameValidate(request, pn, "DOI(Digital Object Identifier)"):
                    return redirect('all_forms', form_no=form_no)

                lwj = request.POST.get('lwj').strip()
                if not va.nameValidate(request, lwj, "Link to website of the Journal"):
                    return redirect('all_forms', form_no=form_no)

                lap = request.POST.get('lap').strip()
                if not va.nameValidate(request, lap, "Link to article/paper/ abstract of the article"):
                    return redirect('all_forms', form_no=form_no)

                lrsj = request.POST.get('lrsj').strip()
                if not va.nameValidate(request, lrsj, "Link to the recognition in SCOPUS enlistment of the Journal"):
                    return redirect('all_forms', form_no=form_no)

                aiop = request.POST.get('aiop').strip()
                if not va.nameValidate(request, aiop, "Affiliating Institute at the time of publication"):
                    return redirect('all_forms', form_no=form_no)

                ssa = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, ssa, "Is SKIT student associated"):
                    return redirect('all_forms', form_no=form_no)

                details = request.POST.get('details').strip()
                if not va.nameValidate(request, details, "If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)"):
                    return redirect('all_forms', form_no=form_no)

                index_by = request.POST.get('optradio1').strip()
                if not va.radiocheck(request, index_by, "Indexed by"):
                    return redirect('all_forms', form_no=form_no)

                quartile = request.POST.get('optradio').strip()
                if not va.radiocheck(request, quartile, "Quartile"):
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', form_no=form_no)

                obj6 = research_journal(noa=noa,top=top,noj=noj,nop=nop,vi=vi,pn=pn,pd=pd,session=session,isnp=isnp,isno=isno,level=level,doi=doi,lwj=lwj,lap=lap,lrsj=lrsj,aiop=aiop,ssa=ssa,details=details,index_by=index_by,quartile=quartile,proof_file=proof_file,email=faculty_instance)
                obj6.save()

            elif form_no == 7:
                noa = request.POST.get('noa').strip()
                if not va.nameValidate(request, noa, "Name of the author(s)"):
                    return redirect('all_forms', form_no=form_no)

                toc = request.POST.get('toc').strip()
                if not va.nameValidate(request, toc, "Title of Conference"):
                    return redirect('all_forms', form_no=form_no)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request, top, "Title of Paper"):
                    return redirect('all_forms', form_no=form_no)

                topc = request.POST.get('topc').strip()
                if not va.nameValidate(request, topc, "Title of the proceedings of the conference"):
                    return redirect('all_forms', form_no=form_no)

                level = request.POST.get('optradio3').strip()
                if not va.nameValidate(request, level, "Level (National/ International)"):
                    return redirect('all_forms', form_no=form_no)

                isnp = request.POST.get('isnp').strip()
                if not va.nameValidate(request, isnp, "ISBN/ISSN number of the proceeding"):
                    return redirect('all_forms', form_no=form_no)

                nop = request.POST.get('nop').strip()
                if not va.nameValidate(request, nop, "Name of the Publisher"):
                    return redirect('all_forms', form_no=form_no)

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                doi = request.POST.get('doi').strip()
                if not va.nameValidate(request, doi, "DOI(Digital Object Identifier)"):
                    return redirect('all_forms', form_no=form_no)

                lwj = request.POST.get('lwj').strip()
                if not va.nameValidate(request, lwj, "Link to website of the Journal"):
                    return redirect('all_forms', form_no=form_no)

                aitp = request.POST.get('aitp').strip()
                if not va.nameValidate(request, aitp, "Affiliating Institute at the time of publication"):
                    return redirect('all_forms', form_no=form_no)

                ssa = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, ssa, "Is SKIT student associated"):
                    return redirect('all_forms', form_no=form_no)

                details = request.POST.get('details').strip()
                if not va.nameValidate(request, details, "If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)"):
                    return redirect('all_forms', form_no=form_no)

                index_by = request.POST.get('index_by').strip()
                if not va.nameValidate(request, index_by, "Indexed by"):
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', form_no=form_no)

                obj7 = research_conference(noa=noa,toc=toc,top=top,topc=topc,level=level,isnp=isnp,nop=nop,pd=pd,session=session,doi=doi,lwj=lwj,aitp=aitp,ssa=ssa,details=details,index_by=index_by,proof_file=proof_file,email=faculty_instance)
                obj7.save()

            elif form_no == 8:
                noa = request.POST.get('noa').strip()
                if not va.nameValidate(request, noa, "Name of the author(s)"):
                    return redirect('all_forms', form_no=form_no)

                tob = request.POST.get('tob').strip()
                if not va.nameValidate(request, tob, "Title of the book"):
                    return redirect('all_forms', form_no=form_no)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request, top, "Title of the chapter Published"):
                    return redirect('all_forms', form_no=form_no)

                level = request.POST.get('optradio3').strip()
                if not va.radiocheck(request, level, "Level (National/ International)"):
                    return redirect('all_forms', form_no=form_no)

                isbn = request.POST.get('isbn').strip()
                if not va.nameValidate(request, isbn, "ISBN"):
                    return redirect('all_forms', form_no=form_no)

                nop = request.POST.get('nop').strip()
                if not va.nameValidate(request, nop, "Name of the Publisher"):
                    return redirect('all_forms', form_no=form_no)

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                doi = request.POST.get('doi').strip()
                if not va.nameValidate(request, doi, "DOI(Digital Object Identifier)"):
                    return redirect('all_forms', form_no=form_no)

                lwj = request.POST.get('lwj').strip()
                if not va.nameValidate(request, lwj, "Link to website of the Journal"):
                    return redirect('all_forms', form_no=form_no)

                aitp = request.POST.get('aitp').strip()
                if not va.nameValidate(request, aitp, "Affiliating Institute at the time of publication"):
                    return redirect('all_forms', form_no=form_no)

                ssa = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, ssa, "Is SKIT student associated"):
                    return redirect('all_forms', form_no=form_no)

                details = request.POST.get('details').strip()
                if not va.nameValidate(request, details, "Write student(s) details"):
                    return redirect('all_forms', form_no=form_no)

                index_by = request.POST.get('index_by').strip()
                if not va.nameValidate(request, index_by, "Indexed by"):
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', form_no=form_no)

                obj8 = research_book(noa=noa,tob=tob,top=top,level=level,isbn=isbn,nop=nop,pd=pd,session=session,doi=doi,lwj=lwj,aitp=aitp,ssa=ssa,details=details,index_by=index_by,proof_file=proof_file,email=faculty_instance)
                obj8.save()

            elif form_no == 9:
                sop = request.POST.get('optradio1').strip()
                if not va.radiocheck(request, sop, "Status of Patent"):
                    return redirect('all_forms', form_no=form_no)

                gi = request.POST.get('nof').strip()
                if not va.nameValidate(request, gi, "Granted ID"):
                    return redirect('all_forms', form_no=form_no)

                ag = request.POST.get('ag').strip()
                if not va.nameValidate(request, ag, "Application ID"):
                    return redirect('all_forms', form_no=form_no)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request, top, "Title of Patent"):
                    return redirect('all_forms', form_no=form_no)

                gc = request.POST.get('gc').strip()
                if not va.nameValidate(request, gc, "Granted Country"):
                    return redirect('all_forms', form_no=form_no)

                pfd = request.POST.get('filed_date')
                try:
                    selected_date = datetime.strptime(pfd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                pg = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, pg, "Type of Patent"):
                    return redirect('all_forms', form_no=form_no)

                ssa = request.POST.get('optradio').strip()
                if not va.radiocheck(request, ssa, "Is SKIT student associated"):
                    return redirect('all_forms', form_no=form_no)

                details = request.POST.get('details').strip()
                if not va.nameValidate(request, details, "Write student(s) details"):
                    return redirect('all_forms', form_no=form_no)

                link = request.POST.get('link').strip()

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', form_no=form_no)

                obj9 = patents(sop=sop,gi=gi, ag=ag, top=top, gc=gc,pfd=pfd, pd=pd, session=session, pg=pg, ssa=ssa, details=details, link=link, proof_file=proof_file,email=faculty_instance)
                obj9.save()

            elif form_no == 10:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request, category, "Category"):
                    return redirect('all_forms', form_no=form_no)

                nos = request.POST.get('nos').strip()
                if not va.nameValidate(request, nos, "Name of the student Guided"):
                    return redirect('all_forms', form_no=form_no)

                ens = request.POST.get('ens').strip()
                if not va.nameValidate(request, ens, "Enrollment Number of Student"):
                    return redirect('all_forms', form_no=form_no)

                urns = request.POST.get('urns').strip()
                if not va.nameValidate(request, urns, "University Roll Number of Student"):
                    return redirect('all_forms', form_no=form_no)

                eys = request.POST.get('enrollmentyear').strip()
                if not va.nameValidate(request, eys, "Enrollment Year of Student"):
                    return redirect('all_forms', form_no=form_no)

                tod = request.POST.get('tod').strip()
                if not va.nameValidate(request, tod, "Title of the Dissertation"):
                    return redirect('all_forms', form_no=form_no)

                visor = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, visor, "Supervisor / Co-supervisor"):
                    return redirect('all_forms', form_no=form_no)

                dov = request.POST.get('dov')
                try:
                    selected_date = datetime.strptime(dov, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                noe = request.POST.get('noe').strip()
                if not va.nameValidate(request, noe, "Name of external examiner"):
                    return redirect('all_forms', form_no=form_no)

                obj10 = guided(category=category ,nos=nos, ens=ens, urns=urns, eys=eys, tod=tod, visor=visor, dov=dov, noe=noe, session=session,email=faculty_instance)
                obj10.save()

            elif form_no == 11:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=form_no)

                toe = request.POST.get('toe').strip()
                if not va.nameValidate(request, toe, "Title of Event/ Exam Name"):
                    return redirect('all_forms', form_no=form_no)

                sa = request.POST.get('sa').strip()
                if not va.nameValidate(request, sa, "Subject Area"):
                    return redirect('all_forms', form_no=form_no)

                doe = int(request.POST.get('doe') or 0)
                if not va.numberValidate(request, doe, "Duration of event (in days)"):
                    return redirect('all_forms', form_no=form_no)

                rpt = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, rpt, "Resource Person Type"):
                    return redirect('all_forms', form_no=form_no)

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                venue = request.POST.get('venue').strip()
                if not va.nameValidate(request, venue, "Venue"):
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', form_no=form_no)

                obj11 = resource(category=category,toe=toe, sa=sa,doe=doe, rpt=rpt, begi_date=begi_date, end_date=end_date, session=session, venue=venue, proof_file=proof_file,email = faculty_instance)
                obj11.save()

            elif form_no == 13:
                payload = jwt.decode(request.POST.get('user_id'), settings.SECRET_KEY, algorithms=["HS256"])
                actual_pk = payload['user_pk']
                faculty_instance = Faculty.objects.get(pk=actual_pk)

                faculty_instance.name = request.POST.get('name').strip()
                if not va.nameValidate(request, faculty_instance.name, "Name"):
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.contact_number = request.POST.get('mobile_no').strip()
                mobilepattern = r'[6789][0-9]{9}'
                if not re.match(mobilepattern, faculty_instance.contact_number):
                    messages.error(request,"Mobile number should start with 6,7,8,9 and should not conatain any alphabets or special characters.")
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.email = request.POST.get('email').strip()

                faculty_instance.gender = request.POST.get('optradio').strip()
                if not va.radiocheck(request, faculty_instance.gender, "Gender"):
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.department = request.POST.get('department').strip()

                faculty_instance.emp_id = int(request.POST.get('emp_id') or 0)
                if not va.numberValidate(request, faculty_instance.emp_id, "Employee ID"):
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.designation = request.POST.get('designation').strip()

                faculty_instance.aos = request.POST.get('aos').strip()
                if not va.radiocheck(request, faculty_instance.aos, "Area of Specialization"):
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.hq = request.POST.get('highest_qualification').strip()
                if not va.radiocheck(request, faculty_instance.hq, "Highest Qualification"):
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.univ_name = request.POST.get('univ_name').strip()
                if not va.nameValidate(request, faculty_instance.univ_name, "University Name"):
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.pshd = request.POST.get('pshd').strip()
                if not va.radiocheck(request, faculty_instance.pshd, "Passing Year of Highest Degree"):
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.pan_no = request.POST.get('pan_no').strip()
                if not va.validate_pan(faculty_instance.pan_no) or not faculty_instance.pan_no:
                    messages.error(request, "Please enter a valid PAN number")
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.dob = request.POST.get('dob')
                try:
                    selected_date = datetime.strptime(faculty_instance.dob, '%Y-%m-%d').date()

                    max_date = datetime.strptime('2001-12-31', '%Y-%m-%d').date()
                    min_date = datetime.strptime('1930-01-01', '%Y-%m-%d').date()

                    if not min_date < selected_date < max_date:
                        messages.error(request,
                                       f"Please select/enter date of birth in range of 1930-01-01 to 2001-12-31.You selected {selected_date}")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date of birth.")
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.jd = request.POST.get('jd')
                try:
                    selected_date = datetime.strptime(faculty_instance.jd,'%Y-%m-%d').date()

                    min_date = datetime.strptime('2000-01-01','%Y-%m-%d').date()

                    if selected_date < min_date:
                        messages.error(request,"Please select/enter date greater than 2000-01-01")
                        return redirect('all_forms',pk=form_no)

                except(ValueError, TypeError):
                    messages.error(request,"Please select/enter a valid date")
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.pd = request.POST.get('pd')
                if faculty_instance.pd == '':
                    faculty_instance.pd = None
                else:
                    try:
                        selected_date = datetime.strptime(faculty_instance.pd, '%Y-%m-%d').date()

                        if selected_date > timezone.now().date():
                            messages.error(request, "Date cannot be in future")
                            return redirect('all_forms', form_no=form_no)

                    except(ValueError, TypeError):
                        messages.error(request, "Please select/enter a valid date")
                        return redirect('all_forms', form_no=form_no)

                faculty_instance.google_scholar = request.POST.get('google_scholar').strip()
                if not va.nameValidate(request, faculty_instance.google_scholar, "Google Scholar"):
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.vidwan_profile = request.POST.get('vidwan_profile').strip()
                if not va.nameValidate(request, faculty_instance.vidwan_profile, "Vidwan Profile"):
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.personal_website_link = request.POST.get('website_link').strip()

                faculty_instance.address = request.POST.get('address').strip()
                if not va.addressValidate(request, faculty_instance.address, "Address"):
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('profile_picture'):
                    profile_picture = request.FILES.get('profile_picture')
                    if not va.imageFileValidate(request, profile_picture, "Profile Picture"):
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.profile_picture = profile_picture

                if request.FILES.get('jr'):
                    jr = request.FILES.get('jr')
                    if not va.fileValidate(request, jr, "Joining Report"):
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.jr = jr

                if request.FILES.get('ol'):
                    of = request.FILES.get('ol')
                    if not va.fileValidate(request, of, "Offer Letter"):
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.of = of

                if request.FILES.get('hdc'):
                    hdc = request.FILES.get('hdc')
                    if not va.fileValidate(request, hdc, "Higher Degree Certificate"):
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.hdc = hdc

                if request.FILES.get('ss'):
                    ss = request.FILES.get('ss')
                    if not va.fileValidate(request, ss, "Salary Slip"):
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.ss = ss

                if request.FILES.get('awards'):
                    certificate = request.FILES.get('awards')
                    if not va.fileValidate(request, certificate, "Co-curricular Certificate"):
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.certificate = certificate

                faculty_instance.phd_univ = request.POST.get('phd_univ').strip()

                phd_dor = request.POST.get('phd_dor')
                if phd_dor == '':
                    faculty_instance.phd_dor = None
                else:
                    try:
                        selected_date = datetime.strptime(phd_dor, '%Y-%m-%d').date()

                        if selected_date > timezone.now().date():
                            messages.error(request, "Date cannot be in future")
                            return redirect('all_forms', form_no=form_no)
                        faculty_instance.phd_dor = phd_dor

                    except(ValueError, TypeError):
                        messages.error(request, "Please select/enter a valid date")
                        return redirect('all_forms', form_no=form_no)

                faculty_instance.norp = int(request.POST.get('norp') or 0)
                if not va.numberValidate(request, faculty_instance.norp, "Number of Research Paper"):
                    return redirect('all_forms', form_no=form_no)
                faculty_instance.status = "R"

                faculty_instance.save()
                messages.success(request,'Profile updated successfully!')

                if request.POST.get('user_id') == Faculty.objects.get(pk=request.session.get('user_id')).pk:
                    return redirect(reverse('editProfile'))
                print("From saveForms pk is: ",request.POST.get('user_id'))
                return redirect('manageProfile', user_token=request.POST.get('user_id'))

            elif form_no == 14:

                faculty_instance = Faculty.objects.get(email=request.POST.get('existing_email'))

                faculty_instance.name = request.POST.get('updated_name').strip()
                if not va.nameValidate(request, faculty_instance.name, "Name"):
                    return redirect(reverse('manage_access'))

                if request.POST.getlist('form_number'):
                    faculty_instance.form_alloted = request.POST.getlist('form_number')

                faculty_instance.contact_number = request.POST.get('updated_number').strip()
                if not va.mobileNumberValidate(request, faculty_instance.contact_number):
                    return redirect(reverse('manage_access'))

                faculty_instance.email = request.POST.get('updated_email').strip()
                if not va.emailValidate(request,faculty_instance.email):
                    return redirect(reverse('manage_access'))

                faculty_instance.department = request.POST.get('updated_department').strip()
                if request.POST.get('updated_role'):
                    faculty_instance.role = request.POST.get('updated_role').strip()
                    faculty_instance.session_version = uuid.uuid4()

                faculty_instance.emp_id = int(request.POST.get('updated_id') or 0)
                if not va.numberValidate(request, faculty_instance.name, "Employee ID"):
                    return redirect(reverse('manage_access'))

                faculty_instance.status = request.POST.get('updated_status').strip()

                faculty_instance.save()
                return redirect(reverse('manage_access'))

            elif form_no == 15:
                emp_id = int(request.POST.get('emp_id') or 0)
                if not va.numberValidate(request, emp_id, "Employee ID"):
                    return redirect(reverse('manage_access'))

                emp_name = request.POST.get('name_per').strip()
                if not va.nameValidate(request, emp_id, "Name"):
                    return redirect(reverse('manage_access'))

                email = request.POST.get('new_email').strip()

                if not va.emailValidate(request, email):
                    return redirect(reverse('manage_access'))

                if Faculty.objects.filter(email=email).exists():
                    messages.error(request, "Email Already Exist")
                    return redirect(reverse('manage_access'))

                department = request.POST.get('selected_department').strip()

                role = request.POST.get('selected_role').strip()

                if request.POST.getlist('form_number'):
                    faculty_instance.form_alloted = request.POST.getlist('form_number')

                con_no = request.POST.get('contact_number').strip()
                if not va.mobileNumberValidate(request, con_no):
                    return redirect(reverse('manage_access'))

                status = request.POST.get('selected_status').strip()

                obj12 = Faculty(name=emp_name,emp_id=emp_id,email=email,department=department,role=role,contact_number=con_no,status=status)
                obj12.save()

                return redirect(reverse('manage_access'))

            return JsonResponse({'status': 'success'})
        # Method not allowed or error saving form
        return render(request, '404.html')

    return render(request,'404.html')

def editforms(request, form_no, user_token):
    if request.method == "POST":
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        actual_pk = payload['user_pk']
        redirect_url = f"/forms_listing/progressdetails/{form_no}/{user_token}"
        if form_no == '1_2':
            instance = non_teaching_staff.objects.get(pk=actual_pk)

            instance.name = request.POST.get('name')
            if not va.nameValidate(request, instance.name, "Name"):
                return redirect(redirect_url)

            instance.mobile_no = request.POST.get('mobile_no')
            if not va.nameValidate(request, instance.mobile_no, "Mobile No"):
                return redirect(redirect_url)

            instance.email = request.POST.get('email')
            if not va.nameValidate(request, instance.email, "Email"):
                return redirect(redirect_url)

            instance.department = request.POST.get('department')
            if not va.radiocheck(request, instance.department, "department"):
                return redirect(redirect_url)

            instance.Lab_no = request.POST.get('Lab_no')
            if not va.numberValidate(request, instance.Lab_no, "Lab No"):
                return redirect(redirect_url)

            instance.designation = request.POST.get('designation')
            if not va.nameValidate(request, instance.designation, "Designation"):
                return redirect(redirect_url)

            instance.emp_id = request.POST.get('emp_id')
            if not va.numberValidate(request, instance.emp_id, "Employee ID"):
                return redirect(redirect_url)

            instance.highest_qual = request.POST.get('highest_qual')
            if not va.radiocheck(request, instance.designation, "Highest Qualification"):
                return redirect(redirect_url)

            instance.university_name = request.POST.get('univ_name')
            if not va.nameValidate(request, instance.emp_id, "University Name"):
                return redirect(redirect_url)

            instance.pshd = request.POST.get('pshd')
            if not va.numberValidate(request, instance.pshd, "Passing Year of Highest Degree"):
                return redirect(redirect_url)

            instance.professional_courses = request.POST.getlist('professional_courses')
            if not va.radiocheck(request, instance.professional_courses, "Professional Courses"):
                return redirect(redirect_url)

            instance.pan_no = request.POST.getlist('pan_no')
            if not va.validate_pan(instance.pan_no):
                return redirect(redirect_url)

            instance.dob = request.POST.get('dob')
            try:
                selected_date = datetime.strptime(instance.dob, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.joining_date = request.POST.get('joining_date')
            try:
                selected_date = datetime.strptime(instance.joining_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.promotion_date = request.POST.get('promotion_date')

            if request.FILES.get('joining_report'):
                joining_report = request.FILES.get('joining_report')
                if not va.fileValidate(request, joining_report, "Joining Report"):
                    return redirect(redirect_url)
                instance.joining_report = joining_report

            if request.FILES.get('offer_letter'):
                offer_letter = request.FILES.get('offer_letter')
                if not va.fileValidate(request, offer_letter, "Offer Letter"):
                    return redirect(redirect_url)
                instance.offer_letter = offer_letter

            if request.FILES.get('higher_degree_certificate'):
                higher_degree_certificate = request.FILES.get('higher_degree_certificate')
                if not va.fileValidate(request, higher_degree_certificate, "Higher Degree Certificate"):
                    return redirect(redirect_url)
                instance.higher_degree_certificate = higher_degree_certificate

            if request.FILES.get('salary_slip'):
                salary_slip = request.FILES.get('salary_slip')
                if not va.fileValidate(request, salary_slip, "Salary Slip"):
                    return redirect(redirect_url)
                instance.salary_slip = salary_slip

            if request.FILES.get('certificate'):
                certificate = request.FILES.get('certificate')
                if not va.fileValidate(request, certificate, "Certificate"):
                    return redirect(redirect_url)
                instance.salary_slip = certificate

            instance.save()

        elif form_no == '2':
            instance = Faculty_participation_data.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            if not va.radiocheck(request, instance.category, "Category"):
                return redirect(redirect_url)

            instance.top = request.POST.get('top').strip()
            if not va.nameValidate(request, instance.top, "Title of Program"):
                return redirect(redirect_url)

            instance.mode = request.POST.get('optradio').strip()
            if not va.radiocheck(request, instance.mode, "Mode"):
                return redirect(redirect_url)

            instance.level = request.POST.get('optradio1').strip()
            if not va.radiocheck(request, instance.level, "Level"):
                return redirect(redirect_url)

            instance.organizer = request.POST.get('organizer').strip()
            if not va.nameValidate(request, instance.organizer, "Organizer"):
                return redirect(redirect_url)

            instance.sponsors = request.POST.get('sponsor').strip()
            if not va.nameValidate(request, instance.sponsors, "Sponsors"):
                return redirect(redirect_url)

            instance.approval = request.POST.get('optradio2').strip()
            if not va.radiocheck(request, instance.approval, "Grant"):
                return redirect(redirect_url)

            instance.begi_date = request.POST.get('begi_date').strip()
            try:
                selected_date = datetime.strptime(instance.begi_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.end_date = request.POST.get('end_date').strip()
            try:
                selected_date = datetime.strptime(instance.end_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Session Year"):
                return redirect(redirect_url)

            instance.no_of_days = request.POST.get('num_of_days')
            if not va.numberValidate(request, instance.no_of_days, "Number of Days"):
                return redirect(redirect_url)

            instance.proof_enclosed = request.POST.get('optradio3').strip()
            if not va.radiocheck(request, instance.proof_enclosed, "Proof Enclosed"):
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '3':
            instance = mooc_course.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            if not va.radiocheck(request, instance.category, "Category"):
                return redirect(redirect_url)

            instance.timeline = request.POST.get('toc').strip()
            if not va.nameValidate(request, instance.timeline, "Timeline of course"):
                return redirect(redirect_url)

            instance.noc = request.POST.get('noc').strip()
            if not va.nameValidate(request, instance.noc, "Name of the Course"):
                return redirect(redirect_url)

            instance.doc = request.POST.get('optradio3').strip()
            if not va.radiocheck(request, instance.noc, "Duration of Course"):
                return redirect(redirect_url)

            instance.begi_date = request.POST.get('begi_date')
            try:
                selected_date = datetime.strptime(instance.begi_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.end_date = request.POST.get('end_date')
            try:
                selected_date = datetime.strptime(instance.end_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.offer = request.POST.get('ofo').strip()
            if not va.nameValidate(request, instance.offer, "Offering Agency/ Organizer"):
                return redirect(redirect_url)

            instance.ctype = request.POST.get('optradio1').strip()
            if not va.radiocheck(request, instance.ctype, "Certificate Type"):
                return redirect(redirect_url)

            instance.topper_in = request.POST.get('optradio2').strip()
            if not va.radiocheck(request, instance.topper_in, "Any category from below"):
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Session"):
                return redirect(redirect_url)

            instance.remarks = request.POST.get('remarks')

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '4':
            instance = events.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            if not va.radiocheck(request, instance.category, "Category"):
                return redirect(redirect_url)

            instance.begi_date = request.POST.get('begi_date')
            try:
                selected_date = datetime.strptime(instance.begi_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.end_date = request.POST.get('end_date')
            try:
                selected_date = datetime.strptime(instance.end_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.nofc = request.POST.get('nofc').strip()
            if not va.nameValidate(request,instance.nofc,"Name of Faculty Coordinator(s)"):
                return redirect(redirect_url)

            instance.eof = request.POST.getlist('optradio3').strip()
            if not va.radiocheck(request,instance.eof,"Event organized for"):
                return redirect(redirect_url)

            instance.topdpo = request.POST.get('topdpo').strip()
            if not va.nameValidate(request,instance.topdpo,"Title of the Professional Development Program Organized"):
                return redirect(redirect_url)

            instance.nop = request.POST.get('nop').strip()
            if not va.nameValidate(request, instance.nop, "No. of participants"):
                return redirect(redirect_url)

            instance.adcc = request.POST.get('acclc').strip()
            if not va.nameValidate(request, instance.adcc, "Academic Department/ Cell/ Committees/ Labs/ COE"):
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Academic Session"):
                return redirect(redirect_url)

            instance.ct = request.POST.get('optradio1').strip()
            if not va.radiocheck(request, instance.ct, "Sponsored/Non Sponsored"):
                return redirect(redirect_url)

            instance.nosa = request.POST.get('nosa').strip()
            if not va.nameValidate(request, instance.nosa, "Name of Sponsoring Agency(if Sponsored)"):
                return redirect(redirect_url)

            instance.cd = request.POST.get('cd').strip()
            if not va.nameValidate(request, instance.cd, "Collaboration Details"):
                return redirect(redirect_url)

            instance.gr = request.POST.get('optradio2').strip()
            if not va.radiocheck(request, instance.gr, "Grant Received(YES/NO)"):
                return redirect(redirect_url)

            instance.gd = request.POST.get('gd').strip()
            if not va.nameValidate(request, instance.gd, "Grant Details"):
                return redirect(redirect_url)

            instance.awpsfooe = request.POST.get('awpsfooe').strip()
            if not va.nameValidate(request, instance.gd, "Association with professional societies for organization of event"):
                return redirect(redirect_url)

            instance.nossp = request.POST.get('nossp').strip()
            if not va.nameValidate(request, instance.nossp,"Number of SKIT students participated"):
                return redirect(redirect_url)

            instance.nosmp = request.POST.get('nosmp').strip()
            if not va.nameValidate(request, instance.nosmp, "Number of staff member participated"):
                return redirect(redirect_url)

            instance.eraipf = request.POST.get('optradio4').strip()
            if not va.radiocheck(request, instance.eraipf, "Event report attached in proper format(YES/NO)"):
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.remarks = request.POST.get('remarks')

            instance.save()

        elif form_no == '5':
            instance = awards_and_achievments.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            if not va.radiocheck(request, instance.category, "Category"):
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Academic Session"):
                return redirect(redirect_url)

            instance.noaa = request.POST.get('noaa').strip()
            if not va.nameValidate(request, instance.noaa, "Name of the Award/   Achievement"):
                return redirect(redirect_url)

            instance.paf = request.POST.get('paf').strip()
            if not va.nameValidate(request, instance.paf, "Position / Award For"):
                return redirect(redirect_url)

            instance.ao = request.POST.get('ao').strip()
            if not va.nameValidate(request, instance.ao, "Agency / Organization"):
                return redirect(redirect_url)

            instance.prize = request.POST.get('prize').strip()
            if not va.nameValidate(request, instance.ao, "Prize"):
                return redirect(redirect_url)

            instance.ad = request.POST.get('prize').strip()
            if not va.nameValidate(request, instance.ad, "Date of Award"):
                return redirect(redirect_url)

            instance.remark = request.POST.get('remark')

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '6':
            instance = sponsored_research.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            if not va.radiocheck(request, instance.category, "Category"):
                return redirect(redirect_url)

            instance.nofa = request.POST.get('nofa').strip()
            if not va.nameValidate(request, instance.nofa, "Name of the Funding Agency"):
                return redirect(redirect_url)

            instance.dop = request.POST.get('dop').strip()
            if not va.nameValidate(request, instance.nofa, "Duration of Project"):
                return redirect(redirect_url)

            instance.amount = request.POST.get('amount').strip()
            if not va.nameValidate(request, instance.amount, "Amount in Rs."):
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Academic Session"):
                return redirect(redirect_url)

            instance.status = request.POST.get('optradio2').strip()
            if not va.radiocheck(request, instance.session, "Status"):
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '7_1':
            instance = research_journal.objects.get(pk=actual_pk)

            instance.noa = request.POST.get('noa').strip()
            if not nameValidate(request,instance.noa,"Name of author"):
                return redirect(redirect_url)

            instance.top = request.POST.get('top').strip()
            if not nameValidate(request, instance.top, "Title of Paper"):
                return redirect(redirect_url)

            instance.noj = request.POST.get('noj').strip()
            if not nameValidate(request, instance.noj, "Name of Journal"):
                return redirect(redirect_url)

            instance.nop = request.POST.get('nop').strip()
            if not nameValidate(request, instance.nop, "Name of the Publisher"):
                return redirect(redirect_url)

            instance.vi = request.POST.get('vi').strip()
            if not nameValidate(request, instance.vi, "Volume, Issue"):
                return redirect(redirect_url)

            instance.pn = request.POST.get('pn').strip()
            if not nameValidate(request, instance.pn, "Page No."):
                return redirect(redirect_url)

            instance.pd = request.POST.get('pd')
            try:
                selected_date = datetime.strptime(instance.pd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Session"):
                return redirect(redirect_url)

            instance.isnp = request.POST.get('isnp').strip()
            if not nameValidate(request, instance.isnp, "ISSN number : Print"):
                return redirect(redirect_url)

            instance.isno = request.POST.get('isno').strip()
            if not nameValidate(request, instance.isno, "ISSN number : Online"):
                return redirect(redirect_url)

            instance.level = request.POST.get('optradio3').strip()
            if not va.radiocheck(request, instance.level, "Level"):
                return redirect(redirect_url)

            instance.doi = request.POST.get('doi').strip()
            if not nameValidate(request, instance.doi, "DOI(Digital Object Identifier)"):
                return redirect(redirect_url)

            instance.lwj = request.POST.get('lwj').strip()
            if not nameValidate(request, instance.lwj, "Link to website of the Journal"):
                return redirect(redirect_url)

            instance.lap = request.POST.get('lap').strip()
            if not nameValidate(request, instance.lap, "Link to article"):
                return redirect(redirect_url)

            instance.lrsj = request.POST.get('lrsj').strip()
            if not nameValidate(request, instance.lrsj, "Link to the recognition"):
                return redirect(redirect_url)

            instance.aiop = request.POST.get('aiop').strip()
            if not nameValidate(request, instance.aiop, "Affiliating Institute"):
                return redirect(redirect_url)

            instance.index_by = request.POST.get('optradio1').strip()
            if not va.radiocheck(request, instance.index_by, "Indexed By"):
                return redirect(redirect_url)

            instance.quartile = request.POST.get('optradio').strip()
            if not va.radiocheck(request, instance.quartile, "Quartile"):
                return redirect(redirect_url)

            instance.ssa = request.POST.get('optradio2').strip()
            if not va.radiocheck(request, instance.index_by, "Is SKIT student associated?"):
                return redirect(redirect_url)

            instance.details = request.POST.get('details').strip()
            if not nameValidate(request, instance.details, "Write student(s) details"):
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '7_2':
            instance = research_conference.objects.get(pk=actual_pk)

            instance.noa = request.POST.get('noa').strip()
            if not nameValidate(request, instance.noa, "Name of author"):
                return redirect(redirect_url)

            instance.toc = request.POST.get('toc').strip()
            if not nameValidate(request, instance.toc, "Title of Conference"):
                return redirect(redirect_url)

            instance.top = request.POST.get('top').strip()
            if not nameValidate(request, instance.top, "Title of Paper"):
                return redirect(redirect_url)

            instance.topc = request.POST.get('topc').strip()
            if not nameValidate(request, instance.topc, "Title of the proceedings of the conference"):
                return redirect(redirect_url)

            instance.level = request.POST.get('optradio3').strip()
            if not radiocheck(request, instance.level, "Level"):
                return redirect(redirect_url)

            instance.ispn = request.POST.get('isbn').strip()
            if not radiocheck(request, instance.level, "ISBN/ISSN number of the proceeding"):
                return redirect(redirect_url)

            instance.nop = request.POST.get('nop').strip()
            if not radiocheck(request, instance.nop, "Name of the Publisher"):
                return redirect(redirect_url)

            instance.pd = request.POST.get('pd')
            try:
                selected_date = datetime.strptime(instance.pd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Academic Session"):
                return redirect(redirect_url)

            instance.doi = request.POST.get('doi').strip()
            if not nameValidate(request, instance.doi, "DOI(Digital Object Identifier)"):
                return redirect(redirect_url)

            instance.lwj = request.POST.get('link').strip()
            if not nameValidate(request, instance.lwj, "Web Link"):
                return redirect(redirect_url)

            instance.aitp = request.POST.get('aiop').strip()
            if not nameValidate(request, instance.aitp, "Affiliating Institute at the time of publication"):
                return redirect(redirect_url)

            instance.ssa = request.POST.get('optradio2').strip()
            if not va.radiocheck(request, instance.index_by, "Is SKIT student associated?"):
                return redirect(redirect_url)

            instance.details = request.POST.get('details').strip()
            if not nameValidate(request, instance.details, "Write student(s) details"):
                return redirect(redirect_url)

            instance.index_by = request.POST.get('index_by').strip()
            if not va.radiocheck(request, instance.index_by, "Indexed By"):
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '7_3':
            instance = research_book.objects.get(pk=actual_pk)

            instance.noa = request.POST.get('noa').strip()
            if not nameValidate(request, instance.noa, "Name of the author/editor"):
                return redirect(redirect_url)

            instance.tob = request.POST.get('tob').strip()
            if not nameValidate(request, instance.tob, "Title of the book"):
                return redirect(redirect_url)

            instance.top = request.POST.get('tocp').strip()
            if not nameValidate(request, instance.top, "Title of the chapter Published"):
                return redirect(redirect_url)

            instance.level = request.POST.get('optradio3').strip()
            if not radiocheck(request, instance.level, "Level"):
                return redirect(redirect_url)

            instance.isbn = request.POST.get('isbn').strip()
            if not nameValidate(request, instance.isbn, "ISBN"):
                return redirect(redirect_url)

            instance.nop = request.POST.get('nop').strip()
            if not nameValidate(request, instance.isbn, "Name of the Publisher"):
                return redirect(redirect_url)

            instance.pd = request.POST.get('pd')
            try:
                selected_date = datetime.strptime(instance.pd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Academic Session"):
                return redirect(redirect_url)

            instance.doi = request.POST.get('doi').strip()
            if not nameValidate(request, instance.doi, "DOI(Digital Object Identifier)"):
                return redirect(redirect_url)

            instance.lwj = request.POST.get('link').strip()
            if not nameValidate(request, instance.lwj, "Web Link"):
                return redirect(redirect_url)

            instance.aitp = request.POST.get('aiop').strip()
            if not nameValidate(request, instance.aitp, "Affiliating Institute at the time of publication"):
                return redirect(redirect_url)

            instance.ssa = request.POST.get('optradio2').strip()
            if not va.radiocheck(request, instance.ssa, "Is SKIT student associated?"):
                return redirect(redirect_url)

            instance.details = request.POST.get('details').strip()
            if not nameValidate(request, instance.details, "Write student(s) details"):
                return redirect(redirect_url)

            instance.index_by = request.POST.get('index_by').strip()
            if not va.radiocheck(request, instance.index_by, "Indexed By"):
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '7_4':
            instance = patents.objects.get(pk=actual_pk)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Academic Session"):
                return redirect(redirect_url)

            instance.sop = request.POST.get('optradio1').strip()
            if not va.radiocheck(request, instance.sop, "Status of Patent"):
                return redirect(redirect_url)

            instance.ag = request.POST.get('aid').strip()
            if not nameValidate(request, instance.ag, "Application ID"):
                return redirect(redirect_url)

            instance.gi = request.POST.get('gd').strip()
            if not nameValidate(request, instance.gi, "Granted ID"):
                return redirect(redirect_url)

            instance.pg = request.POST.get('optradio2').strip()
            if not radiocheck(request, instance.pg, "Type of Patent"):
                return redirect(redirect_url)

            instance.top = request.POST.get('top').strip()
            if not nameValidate(request, instance.details, "Title of Patent"):
                return redirect(redirect_url)

            instance.gc = request.POST.get('gc').strip()
            if not nameValidate(request, instance.gc, "Granted Country"):
                return redirect(redirect_url)

            instance.pfd = request.POST.get('pfd')
            try:
                selected_date = datetime.strptime(instance.pfd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.pd = request.POST.get('pd')
            try:
                selected_date = datetime.strptime(instance.pd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Academic Session"):
                return redirect(redirect_url)

            instance.ssa = request.POST.get('optradio2').strip()
            if not va.radiocheck(request, instance.ssa, "Is SKIT student associated?"):
                return redirect(redirect_url)

            instance.details = request.POST.get('details').strip()
            if not nameValidate(request, instance.details, "Write student(s) details"):
                return redirect(redirect_url)

            instance.link = request.POST.get('link').strip()
            if not nameValidate(request, instance.link, "Web Link"):
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

        elif form_no == '8':
            instance = guided.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            if not va.radiocheck(request, instance.category, "Category"):
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Academic Session"):
                return redirect(redirect_url)

            instance.nos = request.POST.get('nos').strip()
            if not nameValidate(request, instance.nos, "Name of the student Guided"):
                return redirect(redirect_url)

            instance.ens = request.POST.get('ens').strip()
            if not va.nameValidate(request, instance.ens, "Enrollment Number of Student"):
                return redirect(redirect_url)

            instance.urns = request.POST.get('urns').strip()
            if not va.nameValidate(request, instance.urns, "University Roll Number of Student"):
                return redirect(redirect_url)

            instance.eys = request.POST.get('eys').strip()
            if not va.nameValidate(request, instance.urns, "Enrollment Year of Student"):
                return redirect(redirect_url)

            instance.tod = request.POST.get('tod').strip()
            if not va.nameValidate(request, instance.tod, "Title of the Dissertation"):
                return redirect(redirect_url)

            instance.visor = request.POST.get('optradio2').strip()
            if not va.nameValidate(request, instance.tod, "Supervisor / Co-supervisor"):
                return redirect(redirect_url)

            instance.dov = request.POST.get('dov')
            try:
                selected_date = datetime.strptime(instance.dov, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.noe = request.POST.get('noe').strip()
            if not va.nameValidate(request, instance.noe, "Name of external examiner"):
                return redirect(redirect_url)

            instance.save()

        elif form_no == '9':
            instance = resource.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            if not va.radiocheck(request, instance.category, "Category"):
                return redirect(redirect_url)

            instance.toe = request.POST.get('toe').strip()
            if not va.nameValidate(request, instance.toe, "Title of Event/ Exam Name"):
                return redirect(redirect_url)

            instance.sa = request.POST.get('sa').strip()
            if not va.nameValidate(request, instance.sa, "Subject Area/Subject Name/Lab Name/Session Name"):
                return redirect(redirect_url)

            instance.rpt = request.POST.get('rpt').strip()
            if not va.radiocheck(request, instance.rpt, "Resource Person Type"):
                return redirect(redirect_url)

            instance.doe = request.POST.get('doe').strip()
            if not va.nameValidate(request, instance.doe, "Duration of event (in days)"):
                return redirect(redirect_url)

            instance.begi_date = request.POST.get('begi_date')
            try:
                selected_date = datetime.strptime(instance.begi_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.end_date = request.POST.get('end_date')
            try:
                selected_date = datetime.strptime(instance.end_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            if not va.radiocheck(request, instance.session, "Academic Session"):
                return redirect(redirect_url)

            instance.venue = request.POST.get('venue').strip()
            if not va.nameValidate(request, instance.sa, "Venue"):
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                if not va.fileValidate(request, proof_file, "Proof File"):
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        messages.success(request,"Entry Updated Successfully!")
        return redirect(redirect_url)
    else:
        messages.error(request,'Method not allowed')
        return render(request, '404.html')