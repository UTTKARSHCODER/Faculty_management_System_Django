import string
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
from firstWebsite.views import session_login_required
import jwt

@session_login_required
def save_all_forms(request, form_no):
    if form_no:
        if request.method == 'POST':

            session = request.POST.get('sessionyear')
            faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))

            if form_no == 16:
                # Non - Teaching Profile
                #  Picture input can also be added on later discussion
                name = request.POST.get('name').strip()
                status, msg = va.nameValidate(name,"Name")
                if not status:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)

                mobile_no = request.POST.get('mobile_no').strip()
                status, msg = va.mobileNumberValidate(mobile_no)
                if not status:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)

                department = request.POST.get('department',"").strip()

                lab_no = request.POST.get('lab_no').strip()
                status, msg = va.nameValidate(lab_no, "Lab Number")
                if not status:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)

                designation = request.POST.get('designation').strip()
                status, msg = va.nameValidate(designation, "Designation")
                if not status:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)

                emp_id = int(request.POST.get('emp_id') or 0)
                status, msg = va.numberValidate(emp_id, "Employee ID")
                if not status:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)

                highest_qual = request.POST.get('highest_qualification').strip()
                status, msg = va.nameValidate(highest_qual, "Highest Qualification")
                if not status:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)

                university_name = request.POST.get('univ_name').strip()
                status, msg = va.nameValidate(university_name, "University Name")
                if not status:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)

                pshd = int(request.POST.get('pshd') or 0)
                # json response sending, but pop-over not coming even after adding sub-for class.
                # for year > current_year
                status, msg = va.pshdValidate(pshd, "Passing Year of Highest Degree")
                if not status:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)

                professional_course = request.POST.getlist('professional_courses')
                status, msg = va.radiocheck(professional_course,"Professional Course")
                if not status:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)

                pan_no = request.POST.get('pan_no').strip()
                print(pan_no)
                status, msg = va.validate_pan(pan_no)
                if not status or not pan_no:
                    messages.error(request, msg)
                    return redirect('all_forms', form_no=form_no)
                dob = request.POST.get('dob')
                try:
                    selected_date = datetime.strptime(dob,'%Y-%m-%d').date()

                    max_date = datetime.strptime('2001-12-31', '%Y-%m-%d').date()
                    min_date = datetime.strptime('1930-01-01','%Y-%m-%d').date()

                    if not min_date < selected_date < max_date:
                        messages.error(request,f"Please select/enter date of birth in range of 1930-01-01 to 2001-12-31.You selected {selected_date}")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request,"Please select/enter a valid date of birth.")
                    return redirect('all_forms', form_no=form_no)

                joining_date = request.POST.get('jd')
                try:
                    selected_date = datetime.strptime(joining_date,'%Y-%m-%d').date()

                    min_date = datetime.strptime('2000-01-01','%Y-%m-%d').date()

                    if selected_date < min_date:
                        messages.error(request,"Please select/enter joining date greater than 2000-01-01")
                        return redirect('all_forms', form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request,"Please select/enter a valid joining date")
                    return redirect('all_forms', form_no=form_no)

                promotion_date = request.POST.get('pd')
                if promotion_date == '':
                    promotion_date = None

                if request.FILES.get('jr'):
                    joining_report = request.FILES['jr']
                    status, msg = va.fileValidate(joining_report,"Joining Report")
                    if not status:
                        messages.error(request, msg)
                        return redirect('all_forms', form_no=form_no)
                else:
                    messages.error(request,"No file selected for joining report. Please select one!")
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('ol'):
                    offer_letter = request.FILES['ol']
                    status, msg = va.fileValidate(offer_letter,"Offer Letter")
                    if not status:
                        messages.error(request, msg)
                        return redirect('all_forms', form_no=form_no)
                else:
                    messages.error(request,"No file selected for offer letter. Please select one!")
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('hdc'):
                    higher_degree_certificate = request.FILES['hdc']
                    status, msg = va.fileValidate(higher_degree_certificate,"Higher Degree Certificate")
                    if not status:
                        messages.error(request, msg)
                        return redirect('all_forms', form_no=form_no)
                else:
                    messages.error(request,"No file selected for higher degree certificate. Please select one!")
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('ss'):
                    salary_slip = request.FILES['ss']
                    status, msg = va.fileValidate(salary_slip,"Salary Slip")
                    if not status:
                        messages.error(request, msg)
                        return redirect('all_forms', form_no=form_no)
                else:
                    salary_slip = None

                if request.FILES.get('awards'):
                    certificate = request.FILES['awards']
                    status, msg = va.fileValidate(certificate,"Co-curricular Certificate")
                    if not status:
                        messages.error(request, msg)
                        return redirect('all_forms', form_no=form_no)
                else:
                    certificate = None

                obj = non_teaching_staff(session=session, name=name, mobile_no=mobile_no, email=faculty_instance, department=department, Lab_no=lab_no, designation=designation, emp_id=emp_id, highest_qual=highest_qual, university_name=university_name, pshd=pshd, professional_course=professional_course, pan_no=pan_no,dob=dob, joining_date=joining_date, promotion_date=promotion_date, joining_report=joining_report, offer_letter=offer_letter, higher_degree_certificate=higher_degree_certificate, salary_slip=salary_slip, certificate=certificate)
                obj.save()
                messages.success(request, 'Form submitted successfully!')
                return redirect(reverse('fdp'))

            elif form_no == 1:
                category = request.POST.get('category').strip()
                status, msg = va.nameValidate(category, "category")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                top = request.POST.get('top').strip()
                status, msg = va.nameValidate(top, "Title of Program")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                mode = request.POST.get('optradio').strip()
                status, msg = va.radiocheck(mode, "Mode")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                level = request.POST.get('optradio1').strip()
                status, msg = va.radiocheck(level, "Level")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                organizer = request.POST.get('organizer').strip()
                status, msg = va.nameValidate(organizer, "Organizer")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                sponser = request.POST.get('sponser').strip()
                status, msg = va.nameValidate(sponser, "Sponsor")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                approval = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(approval, "(SKIT approved)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        return JsonResponse({'success' : False, 'message' : "From Date cannot be in future"})
                    begi_date = selected_date

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid From date"})

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "To Date cannot be in future")
                        return JsonResponse({'success' : False, 'message' : msg})
                    end_date = selected_date

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid To date"})

                num_of_days = (end_date - begi_date).days

                proof_approval = request.POST.get('optradio3').strip()
                status, msg = va.radiocheck(proof_approval, "Proof Approval")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                if request.FILES.get('proof_file'):
                    proof_file_path = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file_path,"Proof File")
                    if not status:
                        return JsonResponse({'success' : False, 'message' : msg})

                obj1 = Faculty_participation_data(category=category,top=top,mode=mode,level=level,organizer=organizer,sponsors=sponser,approval=approval,begi_date=begi_date,end_date=end_date,session=session,no_of_days=num_of_days,proof_enclosed=proof_approval,proof_file=proof_file_path,email=faculty_instance)
                obj1.save()

            elif form_no == 2:
                category = request.POST.get('category').strip()
                status, msg = va.nameValidate(category, "Category")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                timeline = request.POST.get('toc').strip()
                status, msg = va.nameValidate(timeline, "Timeline")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                noc = request.POST.get('noc').strip()
                status, msg = va.nameValidate(noc, "Name of the Course")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                doc = request.POST.get('optradio3').strip()
                status, msg = va.nameValidate(doc, "Duration of Course")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "From Date cannot be in future")
                        return JsonResponse({'success' : False, 'message' : msg})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid From date"})

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "To Date cannot be in future")
                        return JsonResponse({'success' : False, 'message' : msg})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid To date"})

                offer = request.POST.get('ofo').strip()
                status, msg = va.nameValidate(offer, "Offering Agency / Organizer")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ctype = request.POST.get('optradio1').strip()
                status, msg = va.radiocheck(ctype, "Certificate Type")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                topper_in = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(topper_in, "Topper Category")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                remarks = request.POST.get('remarks').strip()

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file,"Proof File")
                    if not status:
                        return JsonResponse({'success' : False, 'message': msg, 'from' : 'file'})

                obj2 = mooc_course(category=category,timeline=timeline,noc=noc,doc=doc,begi_date=begi_date,end_date=end_date,offer=offer,ctype=ctype,topper_in=topper_in,session=session,remarks=remarks,proof_file=proof_file,email=faculty_instance)
                obj2.save()

            elif form_no == 3:
                category = request.POST.get('category').strip()
                status, msg = va.nameValidate(category, "Category")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                eof = request.POST.getlist('optradio3')
                status, msg = va.radiocheck(eof, "Event organized for")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nofc = request.POST.get('nofc').strip()
                status, msg = va.nameValidate(nofc, "Number of Faculty Coordinators")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                topdpo = request.POST.get('topdpo').strip()
                status, msg = va.nameValidate(topdpo, "Title of the Professional Development Program Organized ")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nop = int(request.POST.get('nop') or 0)
                status, msg = va.numberValidate(nop, "Number of participants")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                adcc = request.POST.get('adcc').strip()
                status, msg = va.nameValidate(adcc, "Academic Department/ Cell / Committees/ Labs /COE ")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ct = request.POST.get('optradio1').strip()
                status, msg = va.radiocheck(ct, "Certificate Type")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nosa = request.POST.get('nosa').strip()
                status, msg = va.nameValidate(nosa, "Name of Sponsoring Agency ")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                cd = request.POST.get('cd').strip()
                status, msg = va.nameValidate(cd, "Collaboration Details")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "From Date cannot be in future")
                        return JsonResponse({'success' : False, 'message' : msg})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid From date"})

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "To Date cannot be in future")
                        return JsonResponse({'success' : False, 'message' : msg})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid To date"})

                gr = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(gr, "Grant Recieved")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                gd = request.POST.get('gd').strip()
                status, msg = va.nameValidate(gd, "Grant Details")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                acutal_expense = request.POST.get('actual_expenditure').strip()
                status, msg = va.nameValidate(acutal_expense, "Actual Expenditure")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                awpsfooe = request.POST.get('awpsfooe').strip()
                status, msg = va.nameValidate(awpsfooe, "Association with professional societies for organization of event")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nossp = request.POST.get('nossp').strip()
                status, msg = va.nameValidate(nossp, "Number of SKIT students participated (Provide list of students with their RTU roll no. & Certificates)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nosmp = request.POST.get('nosmp').strip()
                status, msg = va.nameValidate(nosmp, "Number of staff member participated")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                mapped_sdg = request.POST.getlist('optradio4')
                status, msg = va.radiocheck(mapped_sdg, "Mapped SDG's")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                eraipf = request.POST.get('optradio5').strip()
                status, msg = va.radiocheck(eraipf, "Event Report attached(Yes/No)")
                if not status:
                    return redirect('all_fomrs',form_no=form_no)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file,"Proof file")
                    if not status:
                        return JsonResponse({'success' : False, 'message' : msg})

                remarks = request.POST.get('remarks')

                obj3 = events(category=category,eof=eof,nofc=nofc,topdpo=topdpo,nop=nop,adcc=adcc,session=session,ct=ct,nosa=nosa,cd=cd,begi_date=begi_date,end_date=end_date,gr=gr,gd=gd,actual_expenditure=acutal_expense,awpsfooe=awpsfooe,nossp=nossp,nosmp=nosmp,map_sdg=mapped_sdg,eraipf=eraipf,proof_file=proof_file,remarks=remarks,email=faculty_instance)
                obj3.save()

            elif form_no == 4:
                category = request.POST.get('category').strip()
                status, msg = va.nameValidate(category, "Category")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                noaa = request.POST.get('noaa').strip()
                status, msg = va.nameValidate(noaa, "Number of Awards and Achievements")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                paf = request.POST.get('paf').strip()
                status, msg = va.nameValidate(paf, "Position / Award For ")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ao = request.POST.get('ao').strip()
                status, msg = va.nameValidate(ao, "Agency / Organization ")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                prize = request.POST.get('prize').strip()
                status, msg = va.nameValidate(prize, "Prize")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ad = request.POST.get('award_date')
                try:
                    selected_date = datetime.strptime(ad, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Award Date cannot be in future")
                        return JsonResponse({'success' : False, 'message' : msg})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid Award date"})

                remark = request.POST.get('remark').strip()

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file,"Proof File")
                    if not status:
                        return JsonResponse({'success' : False, 'message' : msg})

                obj4 = awards_and_achievments(category=category,noaa=noaa,paf=paf,ao=ao,prize=prize,ad=ad,remark=remark,session=session,proof_file=proof_file,email=faculty_instance)
                obj4.save()

            elif form_no == 5:
                category = request.POST.get('category').strip()
                status, msg = va.nameValidate(category, "Category")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nofa = request.POST.get('nofa').strip()
                status, msg = va.nameValidate(nofa, " Name of the funding agency ")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                dop = int(request.POST.get('dop') or 0)
                status, msg = va.numberValidate(nofa, "Duration of project")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                amount = int(request.POST.get('amount') or 0)
                status, msg = va.numberValidate(amount, "Amount")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                status = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(status, "Status")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file,"Proof File")
                    if not status:
                        return JsonResponse({'success' : False, 'message' : msg})

                obj5 = sponsored_research(category=category,nofa=nofa,dop=dop,amount=amount,session=session,status=status,proof_file=proof_file,email=faculty_instance)
                obj5.save()

            elif form_no == 6:
                noa = request.POST.get('noa').strip()
                status, msg = va.nameValidate(noa, "Name of the author(s)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                top = request.POST.get('top').strip()
                status, msg = va.nameValidate(top, "Title of paper")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                noj = request.POST.get('noj').strip()
                status, msg = va.nameValidate(noj, "Name of journal")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nop = request.POST.get('nop').strip()
                status, msg = va.nameValidate(nop, "Name of the publisher")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                vi = request.POST.get('vi').strip()
                status, msg = va.nameValidate(vi, "Volume Issue")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                pn = request.POST.get('pn').strip()
                status, msg = va.nameValidate(pn, "Page No.")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Published Date cannot be in future")
                        return JsonResponse({'success' : False, 'message' : msg})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid Published date"})

                isnp = request.POST.get('isnp').strip()
                status, msg = va.nameValidate(isnp, "ISSN number : Print")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                isno = request.POST.get('isno').strip()
                status, msg = va.nameValidate(isno, "ISSN number : Online")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                level = request.POST.get('optradio3').strip()
                status, msg = va.nameValidate(level, "Level(National/ International)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                doi = request.POST.get('doi').strip()
                status, msg = va.nameValidate(doi, "DOI(Digital Object Identifier)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                lwj = request.POST.get('lwj').strip()
                status, msg = va.nameValidate(lwj, "Link to website of the Journal")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                lap = request.POST.get('lap').strip()
                status, msg = va.nameValidate(lap, "Link to article/paper/ abstract of the article")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                lrsj = request.POST.get('lrsj').strip()
                status, msg = va.nameValidate(lrsj, "Link to the recognition in SCOPUS enlistment of the Journal")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                aiop = request.POST.get('aiop').strip()
                status, msg = va.nameValidate(aiop, "Affiliating Institute at the time of publication")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ssa = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(ssa, "Is SKIT student associated?")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                details = request.POST.get('details').strip()
                status, msg = va.nameValidate(details, "If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                index_by = request.POST.get('optradio1').strip()
                status, msg = va.radiocheck(index_by, "Indexed by")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                quartile = request.POST.get('optradio').strip()
                status, msg = va.radiocheck(quartile, "Quartile")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file, "Proof File")
                    if not status:
                        return JsonResponse({'success' : False, 'message' : msg})

                obj6 = research_journal(noa=noa,top=top,noj=noj,nop=nop,vi=vi,pn=pn,pd=pd,session=session,isnp=isnp,isno=isno,level=level,doi=doi,lwj=lwj,lap=lap,lrsj=lrsj,aiop=aiop,ssa=ssa,details=details,index_by=index_by,quartile=quartile,proof_file=proof_file,email=faculty_instance)
                obj6.save()

            elif form_no == 7:
                noa = request.POST.get('noa').strip()
                status, msg = va.nameValidate(noa, "Name of the author(s)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                toc = request.POST.get('toc').strip()
                status, msg = va.nameValidate(toc, "Title of Conference")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                top = request.POST.get('top').strip()
                status, msg = va.nameValidate(top, "Title of Paper")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                topc = request.POST.get('topc').strip()
                status, msg = va.nameValidate(topc, "Title of the proceedings of the conference")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                level = request.POST.get('optradio3').strip()
                status, msg = va.nameValidate(level, "Level (National/ International)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                isnp = request.POST.get('isnp').strip()
                status, msg = va.nameValidate(isnp, "ISBN/ISSN number of the proceeding")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nop = request.POST.get('nop').strip()
                status, msg = va.nameValidate(nop, "Name of the Publisher")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Published Date cannot be in future")
                        return JsonResponse({'success' : False, 'message' : msg})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid Published date"})

                doi = request.POST.get('doi').strip()
                status, msg = va.nameValidate(doi, "DOI(Digital Object Identifier)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                lwj = request.POST.get('lwj').strip()
                status, msg = va.nameValidate(lwj, "Link to website of the Journal")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                aitp = request.POST.get('aitp').strip()
                status, msg = va.nameValidate(aitp, "Affiliating Institute at the time of publication")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ssa = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(ssa, "Is SKIT student associated")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                details = request.POST.get('details').strip()
                status, msg = va.nameValidate(details, "If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                index_by = request.POST.get('index_by').strip()
                status, msg = va.nameValidate(index_by, "Indexed by")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file, "Proof File")
                    if not status:
                        return JsonResponse({'success' : False, 'message' : msg})

                obj7 = research_conference(noa=noa,toc=toc,top=top,topc=topc,level=level,isnp=isnp,nop=nop,pd=pd,session=session,doi=doi,lwj=lwj,aitp=aitp,ssa=ssa,details=details,index_by=index_by,proof_file=proof_file,email=faculty_instance)
                obj7.save()

            elif form_no == 8:
                noa = request.POST.get('noa').strip()
                status, msg = va.nameValidate(noa, "Name of the author(s)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                tob = request.POST.get('tob').strip()
                status, msg = va.nameValidate(tob, "Title of the book")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                top = request.POST.get('top').strip()
                status, msg = va.nameValidate(top, "Title of the chapter Published")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                level = request.POST.get('optradio3').strip()
                status, msg = va.radiocheck(level, "Level (National/ International)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                isbn = request.POST.get('isbn').strip()
                status, msg = va.nameValidate(isbn, "ISBN")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nop = request.POST.get('nop').strip()
                status, msg = va.nameValidate(nop, "Name of the Publisher")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Published Date cannot be in future")
                        return JsonResponse({'success' : False, 'message' : msg})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid Published date"})

                doi = request.POST.get('doi').strip()
                status, msg = va.nameValidate(doi, "DOI(Digital Object Identifier)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                lwj = request.POST.get('lwj').strip()
                status, msg = va.nameValidate(lwj, "Link to website of the Journal")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                aitp = request.POST.get('aitp').strip()
                status, msg = va.nameValidate(aitp, "Affiliating Institute at the time of publication")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ssa = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(ssa, "Is SKIT student associated")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                details = request.POST.get('details').strip()
                status, msg = va.nameValidate(details, "Write student(s) details")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                index_by = request.POST.get('index_by').strip()
                status, msg = va.nameValidate(index_by, "Indexed by")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file, "Proof File")
                    if not status:
                        return JsonResponse({'success' : False, 'message' : msg})

                obj8 = research_book(noa=noa,tob=tob,top=top,level=level,isbn=isbn,nop=nop,pd=pd,session=session,doi=doi,lwj=lwj,aitp=aitp,ssa=ssa,details=details,index_by=index_by,proof_file=proof_file,email=faculty_instance)
                obj8.save()

            elif form_no == 9:
                sop = request.POST.get('optradio1').strip()
                status, msg = va.radiocheck(sop, "Status of Patent")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                gi = request.POST.get('nof').strip()
                status, msg = va.nameValidate(gi, "Granted ID")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ag = request.POST.get('ag').strip()
                status, msg = va.nameValidate(ag, "Application ID")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                top = request.POST.get('top').strip()
                status, msg = va.nameValidate(top, "Title of Patent")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                gc = request.POST.get('gc').strip()
                status, msg = va.nameValidate(gc, "Granted Country")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                pfd = request.POST.get('filed_date')
                try:
                    selected_date = datetime.strptime(pfd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        return JsonResponse({'success' : False, 'message' : "Filed Date cannot be in future"})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid Filed date"})

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        return JsonResponse({'success' : False, 'message' : "Start Date cannot be in future"})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid Start date"})

                pg = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(pg, "Type of Patent")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ssa = request.POST.get('optradio').strip()
                status, msg = va.radiocheck(ssa, "Is SKIT student associated")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                details = request.POST.get('details').strip()
                status, msg = va.nameValidate(details, "Write student(s) details")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                link = request.POST.get('link').strip()

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file, "Proof File")
                    if not status:
                        return JsonResponse({'success' : False, 'message' : msg})

                obj9 = patents(sop=sop,gi=gi, ag=ag, top=top, gc=gc,pfd=pfd, pd=pd, session=session, pg=pg, ssa=ssa, details=details, link=link, proof_file=proof_file,email=faculty_instance)
                obj9.save()

            elif form_no == 10:
                category = request.POST.get('category').strip()
                status, msg = va.nameValidate(category, "Category")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                nos = request.POST.get('nos').strip()
                status, msg = va.nameValidate(nos, "Name of the student Guided")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                ens = request.POST.get('ens').strip()
                status, msg = va.nameValidate(ens, "Enrollment Number of Student")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                urns = request.POST.get('urns').strip()
                status, msg = va.nameValidate(urns, "University Roll Number of Student")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                eys = request.POST.get('enrollmentyear').strip()
                status, msg = va.nameValidate(eys, "Enrollment Year of Student")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                tod = request.POST.get('tod').strip()
                status, msg = va.nameValidate(tod, "Title of the Dissertation")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                visor = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(visor, "Supervisor / Co-supervisor")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                dov = request.POST.get('dov')
                try:
                    selected_date = datetime.strptime(dov, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        return JsonResponse({'success' : False, 'message' : "Viva-Voice Date cannot be in future"})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid date of viva-voice"})

                noe = request.POST.get('noe').strip()
                status, msg = va.nameValidate(noe, "Name of external examiner")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                obj10 = guided(category=category ,nos=nos, ens=ens, urns=urns, eys=eys, tod=tod, visor=visor, dov=dov, noe=noe, session=session,email=faculty_instance)
                obj10.save()

            elif form_no == 11:
                category = request.POST.get('category').strip()
                status, msg = va.nameValidate(category, "Category")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                toe = request.POST.get('toe').strip()
                status, msg = va.nameValidate(toe, "Title of Event/ Exam Name")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                sa = request.POST.get('sa').strip()
                status, msg = va.nameValidate(sa, "Subject Area")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                doe = int(request.POST.get('doe') or 0)
                status, msg = va.numberValidate(doe, "Duration of event (in days)")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                rpt = request.POST.get('optradio2').strip()
                status, msg = va.radiocheck(rpt, "Resource Person Type")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        return JsonResponse({'success' : False, 'message' : "Start Date cannot be in future"})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid start date"})

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        return JsonResponse({'success' : False, 'message' : "End Date cannot be in future"})

                except(ValueError, TypeError):
                    return JsonResponse({'success' : False, 'message' : "Please select/enter a valid end date"})

                venue = request.POST.get('venue').strip()
                status, msg = va.nameValidate(venue, "Venue")
                if not status:
                    return JsonResponse({'success' : False, 'message' : msg})

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    status, msg = va.fileValidate(proof_file, "Proof File")
                    if not status:
                        return JsonResponse({'success' : False, 'message' : msg})

                obj11 = resource(category=category,toe=toe, sa=sa,doe=doe, rpt=rpt, begi_date=begi_date, end_date=end_date, session=session, venue=venue, proof_file=proof_file,email = faculty_instance)
                obj11.save()

            elif form_no == 13:
                # Edit Profile
                payload = jwt.decode(request.POST.get('user_id'), settings.SECRET_KEY, algorithms=["HS256"])
                actual_pk = payload['user_pk']
                faculty_instance = Faculty.objects.get(pk=actual_pk)

                faculty_instance.name = string.capwords(request.POST.get('name').strip())
                status, msg = va.nameValidate(faculty_instance.name, "Name")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.contact_number = request.POST.get('mobile_no').strip()
                mobilepattern = r'[6789][0-9]{9}'
                if not re.match(mobilepattern, faculty_instance.contact_number):
                    messages.error(request,"Mobile number should start with 6,7,8,9 and should not conatain any alphabets or special characters.")
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.email = request.POST.get('email').strip()

                faculty_instance.gender = request.POST.get('optradio').strip()
                status, msg = va.radiocheck(faculty_instance.gender, "Gender")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.department = request.POST.get('department').strip()

                faculty_instance.emp_id = int(request.POST.get('emp_id') or 0)
                status, msg = va.numberValidate(faculty_instance.emp_id, "Employee ID")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.designation = request.POST.get('designation').strip()

                faculty_instance.aos = request.POST.get('aos').strip()
                status, msg = va.radiocheck(faculty_instance.aos, "Area of Specialization")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.hq = request.POST.get('highest_qualification').strip()
                status, msg = va.radiocheck(faculty_instance.hq, "Highest Qualification")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.univ_name = request.POST.get('univ_name').strip()
                status, msg = va.nameValidate(faculty_instance.univ_name, "University Name")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.pshd = int(request.POST.get('pshd') or 0)
                # json response sending, but pop-over not coming even after adding sub-for class.
                # for year > current_year
                status, msg = va.pshdValidate(faculty_instance.pshd, "Passing Year of Highest Degree")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.pan_no = request.POST.get('pan_no').strip()
                status, msg = va.validate_pan(faculty_instance.pan_no)
                if not status or not faculty_instance.pan_no:
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
                        messages.error(request,"Please select/enter joining date greater than 2000-01-01")
                        return redirect('all_forms',form_no=form_no)

                except(ValueError, TypeError):
                    messages.error(request,"Please select/enter a valid Joining date")
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.pd = request.POST.get('pd')
                if faculty_instance.pd == '':
                    faculty_instance.pd = None
                else:
                    try:
                        selected_date = datetime.strptime(faculty_instance.pd, '%Y-%m-%d').date()

                        if selected_date > timezone.now().date():
                            messages.error(request, "Promotion Date cannot be in future")
                            return redirect('all_forms', form_no=form_no)

                    except(ValueError, TypeError):
                        messages.error(request, "Please select/enter a valid promotion date")
                        return redirect('all_forms', form_no=form_no)

                faculty_instance.google_scholar = request.POST.get('google_scholar').strip()
                status, msg = va.nameValidate(faculty_instance.google_scholar, "Google Scholar")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.vidwan_profile = request.POST.get('vidwan_profile').strip()
                status, msg = va.nameValidate(faculty_instance.vidwan_profile, "Vidwan Profile")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                faculty_instance.personal_website_link = request.POST.get('website_link').strip()

                faculty_instance.address = request.POST.get('address').strip()
                status, msg = va.addressValidate(faculty_instance.address, "Address")
                if not status:
                    return redirect('all_forms', form_no=form_no)

                if request.FILES.get('profile_picture'):
                    profile_picture = request.FILES.get('profile_picture')
                    status, msg = va.imageFileValidate(profile_picture, "Profile Picture")
                    if not status:
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.profile_picture = profile_picture

                if request.FILES.get('jr'):
                    jr = request.FILES.get('jr')
                    status, msg = va.fileValidate(jr, "Joining Report")
                    if not status:
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.jr = jr

                if request.FILES.get('ol'):
                    of = request.FILES.get('ol')
                    status, msg = va.fileValidate(of, "Offer Letter")
                    if not status:
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.of = of

                if request.FILES.get('hdc'):
                    hdc = request.FILES.get('hdc')
                    status, msg = va.fileValidate(hdc, "Higher Degree Certificate")
                    if not status:
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.hdc = hdc

                if request.FILES.get('ss'):
                    ss = request.FILES.get('ss')
                    status, msg = va.fileValidate(ss, "Salary Slip")
                    if not status:
                        return redirect('all_forms', form_no=form_no)
                    faculty_instance.ss = ss

                if request.FILES.get('awards'):
                    certificate = request.FILES.get('awards')
                    status, msg = va.fileValidate(certificate, "Co-curricular Certificate")
                    if not status:
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
                            messages.error(request, "PH.D Registration Date cannot be in future")
                            return redirect('all_forms', form_no=form_no)
                        faculty_instance.phd_dor = phd_dor

                    except(ValueError, TypeError):
                        messages.error(request, "Please select/enter a valid phd registration date")
                        return redirect('all_forms', form_no=form_no)

                faculty_instance.norp = int(request.POST.get('norp') or 0)
                status, msg = va.numberValidate(faculty_instance.norp, "Number of Research Paper")
                if not status:
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
                status, msg = va.nameValidate(faculty_instance.name, "Name")
                if not status:
                    return redirect(reverse('manage_access'))

                if request.POST.getlist('form_number'):
                    faculty_instance.form_alloted = request.POST.getlist('form_number')

                faculty_instance.contact_number = request.POST.get('updated_number').strip()
                status, msg = va.mobileNumberValidate(faculty_instance.contact_number)
                if not status:
                    return redirect(reverse('manage_access'))

                faculty_instance.email = request.POST.get('updated_email').strip()
                status, msg = va.emailValidate(faculty_instance.email)
                if not status:
                    return redirect(reverse('manage_access'))

                faculty_instance.department = request.POST.get('updated_department').strip()
                if request.POST.get('updated_role'):
                    faculty_instance.role = request.POST.get('updated_role').strip()
                    faculty_instance.session_version = uuid.uuid4()

                faculty_instance.emp_id = int(request.POST.get('updated_id') or 0)
                status, msg = va.numberValidate(faculty_instance.emp_id, "Employee ID")
                if not status:
                    return redirect(reverse('manage_access'))

                faculty_instance.status = request.POST.get('updated_status').strip()

                faculty_instance.save()
                return redirect(reverse('manage_access'))

            elif form_no == 15:
                emp_id = int(request.POST.get('emp_id') or 0)
                status, msg = va.numberValidate(emp_id, "Employee ID")
                if not status:
                    return redirect(reverse('manage_access'))

                emp_name = request.POST.get('name_per').strip()
                status, msg = va.nameValidate(emp_name, "Name")
                if not status:
                    return redirect(reverse('manage_access'))

                email = request.POST.get('new_email').strip()

                status, msg = va.emailValidate(email)
                if not status:
                    return redirect(reverse('manage_access'))

                if Faculty.objects.filter(email=email).exists():
                    messages.error(request, "Email Already Exist")
                    return redirect(reverse('manage_access'))

                department = request.POST.get('selected_department').strip()

                role = request.POST.get('selected_role').strip()

                if request.POST.getlist('form_number'):
                    faculty_instance.form_alloted = request.POST.getlist('form_number')

                con_no = request.POST.get('contact_number').strip()
                status, msg = va.mobileNumberValidate(con_no)
                if not status:
                    return redirect(reverse('manage_access'))

                status = request.POST.get('selected_status').strip()

                obj12 = Faculty(name=emp_name,emp_id=emp_id,email=email,department=department,role=role,contact_number=con_no,status=status)
                obj12.save()

                return redirect(reverse('manage_access'))

            return JsonResponse({'success': True, 'message' : 'Form submitted successfully!'})
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
            status, msg = va.nameValidate(instance.name, "Name")
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.mobile_no = request.POST.get('mobile_no')
            status, msg = va.mobileNumberValidate(instance.mobile_no)
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            # instance.email = request.POST.get('email')
            # status, msg = va.nameValidate(instance.email, "Email")
            # if not status:
            #     return redirect(redirect_url)

            instance.department = request.POST.get('department')
            status, msg = va.radiocheck(instance.department, "department")
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.Lab_no = request.POST.get('Lab_no')
            status, msg = va.nameValidate(instance.Lab_no, "Lab No")
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.designation = request.POST.get('designation')
            status, msg = va.nameValidate(instance.designation, "Designation")
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.emp_id = request.POST.get('emp_id')
            status, msg = va.numberValidate(instance.emp_id, "Employee ID")
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.highest_qual = request.POST.get('highest_qualification')
            status, msg = va.radiocheck(instance.highest_qual, "Highest Qualification")
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.university_name = request.POST.get('univ_name')
            status, msg = va.nameValidate(instance.university_name, "University Name")
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.pshd = int(request.POST.get('pshd') or 0)
            # json response sending, but pop-over not coming even after adding sub-for class.
            # for year > current_year
            status, msg = va.pshdValidate(instance.pshd, "Passing Year of Highest Degree")
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.professional_course = request.POST.getlist('professional_courses')
            print(instance.professional_course)
            status, msg = va.radiocheck(instance.professional_course, "Professional Course")
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.pan_no = request.POST.get('pan_no')
            status, msg = va.validate_pan(instance.pan_no)
            if not status:
                messages.error(request, msg)
                return redirect(redirect_url)

            instance.dob = request.POST.get('dob')
            try:
                selected_date = datetime.strptime(instance.dob, '%Y-%m-%d').date()

                min_date = datetime.strptime('1926-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date of birth greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date of birth.")
                return redirect(redirect_url)

            instance.joining_date = request.POST.get('joining_date')
            try:
                selected_date = datetime.strptime(instance.joining_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter joining date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid joining date")
                return redirect(redirect_url)

            instance.promotion_date = request.POST.get('promotion_date')

            if request.FILES.get('joining_report'):
                joining_report = request.FILES.get('joining_report')
                status, msg = va.fileValidate(joining_report, "Joining Report")
                if not status:
                    messages.error(request, msg)
                    return redirect(redirect_url)
                instance.joining_report = joining_report

            if request.FILES.get('offer_letter'):
                offer_letter = request.FILES.get('offer_letter')
                status, msg = va.fileValidate(offer_letter, "Offer Letter")
                if not status:
                    messages.error(request, msg)
                    return redirect(redirect_url)
                instance.offer_letter = offer_letter

            if request.FILES.get('higher_degree_certificate'):
                higher_degree_certificate = request.FILES.get('higher_degree_certificate')
                status, msg = va.fileValidate(higher_degree_certificate, "Higher Degree Certificate")
                if not status:
                    messages.error(request, msg)
                    return redirect(redirect_url)
                instance.higher_degree_certificate = higher_degree_certificate

            if request.FILES.get('salary_slip'):
                salary_slip = request.FILES.get('salary_slip')
                status, msg = va.fileValidate(salary_slip, "Salary Slip")
                if not status:
                    messages.error(request, msg)
                    return redirect(redirect_url)
                instance.salary_slip = salary_slip

            if request.FILES.get('certificate'):
                certificate = request.FILES.get('certificate')
                status, msg = va.fileValidate(certificate, "Certificate")
                if not status:
                    messages.error(request, msg)
                    return redirect(redirect_url)
                instance.salary_slip = certificate

            instance.save()

        elif form_no == '2':
            instance = Faculty_participation_data.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            status, msg = va.radiocheck(instance.category, "Category")
            if not status:
                return redirect(redirect_url)

            instance.top = request.POST.get('top').strip()
            status, msg = va.nameValidate(instance.top, "Title of Program")
            if not status:
                return redirect(redirect_url)

            instance.mode = request.POST.get('optradio').strip()
            status, msg = va.radiocheck(instance.mode, "Mode")
            if not status:
                return redirect(redirect_url)

            instance.level = request.POST.get('optradio1').strip()
            status, msg = va.radiocheck(instance.level, "Level")
            if not status:
                return redirect(redirect_url)

            instance.organizer = request.POST.get('organizer').strip()
            status, msg = va.nameValidate(instance.organizer, "Organizer")
            if not status:
                return redirect(redirect_url)

            instance.sponsors = request.POST.get('sponsor').strip()
            status, msg = va.nameValidate(instance.sponsors, "Sponsors")
            if not status:
                return redirect(redirect_url)

            instance.approval = request.POST.get('optradio2').strip()
            status, msg = va.radiocheck(instance.approval, "Grant")
            if not status:
                return redirect(redirect_url)

            instance.begi_date = request.POST.get('begi_date').strip()
            try:
                selected_date = datetime.strptime(instance.begi_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter From date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid From date")
                return redirect(redirect_url)

            instance.end_date = request.POST.get('end_date').strip()
            try:
                selected_date = datetime.strptime(instance.end_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter To date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid To date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Session Year")
            if not status:
                return redirect(redirect_url)

            instance.no_of_days = request.POST.get('num_of_days')
            status, msg = va.numberValidate(instance.no_of_days, "Number of Days")
            if not status:
                return redirect(redirect_url)

            instance.proof_enclosed = request.POST.get('optradio3').strip()
            status, msg = va.radiocheck(instance.proof_enclosed, "Proof Enclosed")
            if not status:
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '3':
            instance = mooc_course.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            status, msg = va.radiocheck(instance.category, "Category")
            if not status:
                return redirect(redirect_url)

            instance.timeline = request.POST.get('toc').strip()
            status, msg = va.nameValidate(instance.timeline, "Timeline of course")
            if not status:
                return redirect(redirect_url)

            instance.noc = request.POST.get('noc').strip()
            status, msg = va.nameValidate(instance.noc, "Name of the Course")
            if not status:
                return redirect(redirect_url)

            instance.doc = request.POST.get('optradio3').strip()
            status, msg = va.radiocheck(instance.doc, "Duration of Course")
            if not status:
                return redirect(redirect_url)

            instance.begi_date = request.POST.get('begi_date')
            try:
                selected_date = datetime.strptime(instance.begi_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter From date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid From date")
                return redirect(redirect_url)

            instance.end_date = request.POST.get('end_date')
            try:
                selected_date = datetime.strptime(instance.end_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter To date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid To date")
                return redirect(redirect_url)

            instance.offer = request.POST.get('ofo').strip()
            status, msg = va.nameValidate(instance.offer, "Offering Agency/ Organizer")
            if not status:
                return redirect(redirect_url)

            instance.ctype = request.POST.get('optradio1').strip()
            status, msg = va.radiocheck(instance.ctype, "Certificate Type")
            if not status:
                return redirect(redirect_url)

            instance.topper_in = request.POST.get('optradio2').strip()
            status, msg = va.radiocheck(instance.topper_in, "Any category from below")
            if not status:
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Session")
            if not status:
                return redirect(redirect_url)

            instance.remarks = request.POST.get('remarks')

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status, msg = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '4':
            instance = events.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            status, msg = va.radiocheck(instance.category, "Category")
            if not status:
                return redirect(redirect_url)

            instance.begi_date = request.POST.get('begi_date')
            try:
                selected_date = datetime.strptime(instance.begi_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter From date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid From date")
                return redirect(redirect_url)

            instance.end_date = request.POST.get('end_date')
            try:
                selected_date = datetime.strptime(instance.end_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter To date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid To date")
                return redirect(redirect_url)

            instance.nofc = request.POST.get('nofc').strip()
            status, msg = va.nameValidate(instance.nofc, "Name of Faculty Coordinator(s)")
            if not status:
                return redirect(redirect_url)

            instance.eof = request.POST.getlist('optradio3')
            status, msg = va.radiocheck(instance.eof, "Event organized for")
            if not status:
                return redirect(redirect_url)

            instance.topdpo = request.POST.get('topdpo').strip()
            status, msg = va.nameValidate(instance.topdpo, "Title of the Professional Development Program Organized")
            if not status:
                return redirect(redirect_url)

            instance.nop = request.POST.get('nop').strip()
            status, msg = va.nameValidate(instance.nop, "No. of participants")
            if not status:
                return redirect(redirect_url)

            instance.adcc = request.POST.get('acclc').strip()
            status, msg = va.nameValidate(instance.adcc, "Academic Department/ Cell/ Committees/ Labs/ COE")
            if not status:
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Academic Session")
            if not status:
                return redirect(redirect_url)

            instance.ct = request.POST.get('optradio1').strip()
            status, msg = va.radiocheck(instance.ct, "Sponsored/Non Sponsored")
            if not status:
                return redirect(redirect_url)

            instance.nosa = request.POST.get('nosa').strip()
            status, msg = va.nameValidate(instance.nosa, "Name of Sponsoring Agency(if Sponsored)")
            if not status:
                return redirect(redirect_url)

            instance.cd = request.POST.get('cd').strip()
            status, msg = va.nameValidate(instance.cd, "Collaboration Details")
            if not status:
                return redirect(redirect_url)

            instance.gr = request.POST.get('optradio2').strip()
            status, msg = va.radiocheck(instance.gr, "Grant Received(YES/NO)")
            if not status:
                return redirect(redirect_url)

            instance.gd = request.POST.get('gd').strip()
            status, msg = va.nameValidate(instance.gd, "Grant Details")
            if not status:
                return redirect(redirect_url)

            instance.awpsfooe = request.POST.get('awpsfooe').strip()
            status, msg = va.nameValidate(instance.awpsfooe, "Association with professional societies for organization of event")
            if not status:
                return redirect(redirect_url)

            instance.nossp = request.POST.get('nossp').strip()
            status, msg = va.nameValidate(instance.nossp, "Number of SKIT students participated")
            if not status:
                return redirect(redirect_url)

            instance.nosmp = request.POST.get('nosmp').strip()
            status, msg = va.nameValidate(instance.nosmp, "Number of staff member participated")
            if not status:
                return redirect(redirect_url)

            instance.eraipf = request.POST.get('optradio4').strip()
            status, msg = va.radiocheck(instance.eraipf, "Event report attached in proper format(YES/NO)")
            if not status:
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status, msg = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.remarks = request.POST.get('remarks')

            instance.save()

        elif form_no == '5':
            instance = awards_and_achievments.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            status, msg = va.radiocheck(instance.category, "Category")
            if not status:
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Academic Session")
            if not status:
                return redirect(redirect_url)

            instance.noaa = request.POST.get('noaa').strip()
            status, msg = va.nameValidate(instance.noaa, "Name of the Award/ Achievement")
            if not status:
                return redirect(redirect_url)

            instance.paf = request.POST.get('paf').strip()
            status, msg = va.nameValidate(instance.paf, "Position / Award For")
            if not status:
                return redirect(redirect_url)

            instance.ao = request.POST.get('ao').strip()
            status, msg = va.nameValidate(instance.ao, "Agency / Organization")
            if not status:
                return redirect(redirect_url)

            instance.prize = request.POST.get('prize').strip()
            status, msg = va.nameValidate(instance.prize, "Prize")
            if not status:
                return redirect(redirect_url)

            instance.ad = request.POST.get('ad')
            try:
                selected_date = datetime.strptime(instance.ad, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter award date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid award date")
                return redirect(redirect_url)

            instance.remark = request.POST.get('remark')

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status, msg = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '6':
            instance = sponsored_research.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            status, msg = va.radiocheck(instance.category, "Category")
            if not status:
                return redirect(redirect_url)

            instance.nofa = request.POST.get('nofa').strip()
            status, msg = va.nameValidate(instance.nofa, "Name of the Funding Agency")
            if not status:
                return redirect(redirect_url)

            instance.dop = request.POST.get('dop').strip()
            status, msg = va.nameValidate(instance.dop, "Duration of Project")
            if not status:
                return redirect(redirect_url)

            instance.amount = request.POST.get('amount').strip()
            status, msg = va.numberValidate(instance.amount, "Amount in Rs.")
            if not status:
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Academic Session")
            if not status:
                return redirect(redirect_url)

            instance.status = request.POST.get('optradio2').strip()
            status, msg = va.radiocheck(instance.status, "Status")
            if not status:
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status, msg = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '7_1':
            instance = research_journal.objects.get(pk=actual_pk)

            instance.noa = request.POST.get('noa').strip()
            status, msg = va.nameValidate(instance.noa, "Name of author")
            if not status:
                return redirect(redirect_url)

            instance.top = request.POST.get('top').strip()
            status, msg = va.nameValidate(instance.top, "Title of Paper")
            if not status:
                return redirect(redirect_url)

            instance.noj = request.POST.get('noj').strip()
            status, msg = va.nameValidate(instance.noj, "Name of Journal")
            if not status:
                return redirect(redirect_url)

            instance.nop = request.POST.get('nop').strip()
            status, msg = va.nameValidate(instance.nop, "Name of the Publisher")
            if not status:
                return redirect(redirect_url)

            instance.vi = request.POST.get('vi').strip()
            status, msg = va.nameValidate(instance.vi, "Volume, Issue")
            if not status:
                return redirect(redirect_url)

            instance.pn = request.POST.get('pn').strip()
            status, msg = va.nameValidate(instance.pn, "Page No.")
            if not status:
                return redirect(redirect_url)

            instance.pd = request.POST.get('pd')
            try:
                selected_date = datetime.strptime(instance.pd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter Published date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid Published date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Session")
            if not status:
                return redirect(redirect_url)

            instance.isnp = request.POST.get('isnp').strip()
            status, msg = va.nameValidate(instance.isnp, "ISSN number : Print")
            if not status:
                return redirect(redirect_url)

            instance.isno = request.POST.get('isno').strip()
            status, msg = va.nameValidate(instance.isno, "ISSN number : Online")
            if not status:
                return redirect(redirect_url)

            instance.level = request.POST.get('optradio3').strip()
            status, msg = va.radiocheck(instance.level, "Level")
            if not status:
                return redirect(redirect_url)

            instance.doi = request.POST.get('doi').strip()
            status, msg = va.nameValidate(instance.doi, "DOI(Digital Object Identifier)")
            if not status:
                return redirect(redirect_url)

            instance.lwj = request.POST.get('lwj').strip()
            status, msg = va.nameValidate(instance.lwj, "Link to website of the Journal")
            if not status:
                return redirect(redirect_url)

            instance.lap = request.POST.get('lap').strip()
            status, msg = va.nameValidate(instance.lap, "Link to article")
            if not status:
                return redirect(redirect_url)

            instance.lrsj = request.POST.get('lrsj').strip()
            status, msg = va.nameValidate(instance.lrsj, "Link to the recognition")
            if not status:
                return redirect(redirect_url)

            instance.aiop = request.POST.get('aiop').strip()
            status, msg = va.nameValidate(instance.aiop, "Affiliating Institute")
            if not status:
                return redirect(redirect_url)

            instance.index_by = request.POST.get('optradio1').strip()
            status, msg = va.radiocheck(instance.index_by, "Index By")
            if not status:
                return redirect(redirect_url)

            instance.quartile = request.POST.get('optradio').strip()
            status, msg = va.radiocheck(instance.quartile, "Quartile")
            if not status:
                return redirect(redirect_url)

            instance.ssa = request.POST.get('optradio2').strip()
            status, msg = va.radiocheck(instance.ssa, "Is SKIT student associated?")
            if not status:
                return redirect(redirect_url)

            instance.details = request.POST.get('details').strip()
            status, msg = va.nameValidate(instance.details, "Write student(s) details")
            if not status:
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status, msg = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '7_2':
            instance = research_conference.objects.get(pk=actual_pk)

            instance.noa = request.POST.get('noa').strip()
            status, msg = va.nameValidate(instance.noa, "Name of author")
            if not status:
                return redirect(redirect_url)

            instance.toc = request.POST.get('toc').strip()
            status, msg = va.nameValidate(instance.toc, "Title of Conference")
            if not status:
                return redirect(redirect_url)

            instance.top = request.POST.get('top').strip()
            status, msg = va.nameValidate(instance.top, "Title of Paper")
            if not status:
                return redirect(redirect_url)

            instance.topc = request.POST.get('topc').strip()
            status, msg = va.nameValidate(instance.topc, "Title of the proceedings of the conference")
            if not status:
                return redirect(redirect_url)

            instance.level = request.POST.get('optradio3').strip()
            status, msg = va.radiocheck(instance.level, "Level")
            if not status:
                return redirect(redirect_url)

            instance.isnp = request.POST.get('isnp').strip()
            status, msg = va.nameValidate(instance.level, "ISBN/ISSN number of the proceeding")
            if not status:
                return redirect(redirect_url)

            instance.nop = request.POST.get('nop').strip()
            status, msg = va.nameValidate(instance.nop, "Name of the Publisher")
            if not status:
                return redirect(redirect_url)

            instance.pd = request.POST.get('pd')
            try:
                selected_date = datetime.strptime(instance.pd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter Published date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid Published date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Academic Session")
            if not status:
                return redirect(redirect_url)

            instance.doi = request.POST.get('doi').strip()
            status, msg = va.nameValidate(instance.doi, "DOI(Digital Object Identifier)")
            if not status:
                return redirect(redirect_url)

            instance.lwj = request.POST.get('lwj').strip()
            status, msg = va.nameValidate(instance.lwj, "Link to website of the Journal")
            if not status:
                return redirect(redirect_url)

            instance.aitp = request.POST.get('aiop').strip()
            status, msg = va.nameValidate(instance.aitp, "Affiliating Institute at the time of publication")
            if not status:
                return redirect(redirect_url)

            instance.ssa = request.POST.get('optradio2').strip()
            status, msg = va.nameValidate(instance.ssa, "Is SKIT student associated?")
            if not status:
                return redirect(redirect_url)

            instance.details = request.POST.get('details').strip()
            status, msg = va.nameValidate(instance.details, "Write student(s) details")
            if not status:
                return redirect(redirect_url)

            instance.index_by = request.POST.get('index_by').strip()
            status, msg = va.radiocheck(instance.index_by, "Indexed By")
            if not status:
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status, msg = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '7_3':
            instance = research_book.objects.get(pk=actual_pk)

            instance.noa = request.POST.get('noa').strip()
            status, msg = va.nameValidate(instance.noa, "Name of author")
            if not status:
                return redirect(redirect_url)

            instance.tob = request.POST.get('tob').strip()
            status, msg = va.nameValidate(instance.tob, "Title of the Book")
            if not status:
                return redirect(redirect_url)

            instance.tocp = request.POST.get('tocp').strip()
            status, msg = va.nameValidate(instance.tocp, "Title of the chapter Published")
            if not status:
                return redirect(redirect_url)

            instance.level = request.POST.get('optradio3').strip()
            sta, msg = va.radiocheck(instance.level, "Level")
            if not status:
                return redirect(redirect_url)

            instance.isbn = request.POST.get('isbn').strip()
            status, msg = va.nameValidate(instance.isbn, "ISBN")
            if not status:
                return redirect(redirect_url)

            instance.nop = request.POST.get('nop').strip()
            status, msg = va.nameValidate(instance.nop, "Name of the Publisher")
            if not status:
                return redirect(redirect_url)

            instance.pd = request.POST.get('pd')
            try:
                selected_date = datetime.strptime(instance.pd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter Published date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid Published date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Academic Session")
            if not status:
                return redirect(redirect_url)

            instance.doi = request.POST.get('doi').strip()
            status, msg = va.nameValidate(instance.doi, "DOI(Digital Object Identifier)")
            if not status:
                return redirect(redirect_url)

            instance.lwj = request.POST.get('lwj').strip()
            status, msg = va.nameValidate(instance.lwj, "Link to website of the Journal")
            if not status:
                return redirect(redirect_url)

            instance.aitp = request.POST.get('aiop').strip()
            status, msg = va.nameValidate(instance.aitp, "Affiliating Institute at the time of publication")
            if not status:
                return redirect(redirect_url)

            instance.ssa = request.POST.get('optradio2').strip()
            status, msg = va.radiocheck(instance.ssa, "Is SKIT student associated?")
            if not status:
                return redirect(redirect_url)

            instance.details = request.POST.get('details').strip()
            status, msg = va.nameValidate(instance.details, "Write student(s) details")
            if not status:
                return redirect(redirect_url)

            instance.index_by = request.POST.get('index_by').strip()
            status, msg = va.nameValidate(instance.index_by, "Indexed By")
            if not status:
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status, msg = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '7_4':
            instance = patents.objects.get(pk=actual_pk)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Academic Session")
            if not status:
                return redirect(redirect_url)

            instance.sop = request.POST.get('optradio1').strip()
            status, msg = va.radiocheck(instance.sop, "Status of Patent")
            if not status:
                return redirect(redirect_url)

            instance.ag = request.POST.get('aid').strip()
            status, msg = va.nameValidate(instance.ag, "Application ID")
            if not status:
                return redirect(redirect_url)

            instance.gi = request.POST.get('gd').strip()
            status, msg = va.nameValidate(instance.gi, "Granted ID")
            if not status:
                return redirect(redirect_url)

            instance.pg = request.POST.get('optradio2').strip()
            status, msg = va.radiocheck(instance.pg, "Type of Patent")
            if not status:
                return redirect(redirect_url)

            instance.top = request.POST.get('top').strip()
            status, msg = va.nameValidate(instance.top, "Title of Patent")
            if not status:
                return redirect(redirect_url)

            instance.gc = request.POST.get('gc').strip()
            status, msg = va.nameValidate(instance.gc, "Granted Country")
            if not status:
                return redirect(redirect_url)

            instance.pfd = request.POST.get('pfd')
            try:
                selected_date = datetime.strptime(instance.pfd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter patent filed date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid patent filed date")
                return redirect(redirect_url)

            instance.pd = request.POST.get('pd')
            try:
                selected_date = datetime.strptime(instance.pd, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter publication date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid publication date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Academic Session")
            if not status:
                return redirect(redirect_url)

            instance.ssa = request.POST.get('optradio').strip()
            status, msg = va.radiocheck(instance.ssa, "Is SKIT student associated?")
            if not status:
                return redirect(redirect_url)

            instance.details = request.POST.get('details').strip()
            status, msg = va.nameValidate(instance.details, "Write student(s) details")
            if not status:
                return redirect(redirect_url)

            instance.link = request.POST.get('link').strip()
            status, msg = va.nameValidate(instance.link, "Web Link")
            if not status:
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status, msg = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        elif form_no == '8':
            instance = guided.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            status, msg = va.radiocheck(instance.category, "Category")
            if not status:
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Academic Session")
            if not status:
                return redirect(redirect_url)

            instance.nos = request.POST.get('nos').strip()
            status, msg = va.nameValidate(instance.nos, "Name of the student Guided")
            if not status:
                return redirect(redirect_url)

            instance.ens = request.POST.get('ens').strip()
            status, msg = va.nameValidate(instance.ens , "Enrollment Number of Student")
            if not status:
                return redirect(redirect_url)

            instance.urns = request.POST.get('urns').strip()
            status, msg = va.nameValidate(instance.urns, "University Roll Number of Student")
            if not status:
                return redirect(redirect_url)

            instance.eys = request.POST.get('eys').strip()
            status, msg = va.nameValidate(instance.eys, "Enrollment Year of Student")
            if not status:
                return redirect(redirect_url)

            instance.tod = request.POST.get('tod').strip()
            status, msg = va.nameValidate(instance.tod, "Title of the Dissertation")
            if not status:
                return redirect(redirect_url)

            instance.visor = request.POST.get('optradio2').strip()
            status, msg = va.nameValidate(instance.visor, "Supervisor / Co-supervisor")
            if not status:
                return redirect(redirect_url)

            instance.dov = request.POST.get('dov')
            try:
                selected_date = datetime.strptime(instance.dov, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter date of viva-voice greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid date of viva-voice")
                return redirect(redirect_url)

            instance.noe = request.POST.get('noe').strip()
            status, msg = va.nameValidate(instance.noe, "Name of external examiner")
            if not status:
                return redirect(redirect_url)

            instance.save()

        elif form_no == '9':
            instance = resource.objects.get(pk=actual_pk)

            instance.category = request.POST.get('category').strip()
            status, msg = va.radiocheck(instance.category, "Category")
            if not status:
                return redirect(redirect_url)

            instance.toe = request.POST.get('toe').strip()
            status, msg = va.nameValidate(instance.toe , "Title of Event/ Exam Name")
            if not status:
                return redirect(redirect_url)

            instance.sa = request.POST.get('sa').strip()
            status, msg = va.nameValidate(instance.sa, "Subject Area/Subject Name/Lab Name/Session Name")
            if not status:
                return redirect(redirect_url)

            instance.rpt = request.POST.get('optradio2').strip()
            status, msg = va.radiocheck(instance.rpt, "Resource Person Type")
            if not status:
                return redirect(redirect_url)

            instance.doe = request.POST.get('doe').strip()
            status, msg = va.nameValidate(instance.doe, "Duration of event (in days)")
            if not status:
                return redirect(redirect_url)

            instance.begi_date = request.POST.get('begi_date')
            try:
                selected_date = datetime.strptime(instance.begi_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter From date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid From date")
                return redirect(redirect_url)

            instance.end_date = request.POST.get('end_date')
            try:
                selected_date = datetime.strptime(instance.end_date, '%Y-%m-%d').date()

                min_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()

                if selected_date < min_date:
                    messages.error(request, "Please select/enter To date greater than 2000-01-01")
                    return redirect(redirect_url)
            except(ValueError, TypeError):
                messages.error(request, "Please select/enter a valid To date")
                return redirect(redirect_url)

            instance.session = request.POST.get('sessionyear').strip()
            status, msg = va.radiocheck(instance.session, "Academic Session")
            if not status:
                return redirect(redirect_url)

            instance.venue = request.POST.get('venue').strip()
            status, msg = va.nameValidate(instance.venue, "Venue")
            if not status:
                return redirect(redirect_url)

            if request.FILES.get('proof_file'):
                proof_file = request.FILES.get('proof_file')
                status, msg = va.fileValidate(proof_file, "Proof File")
                if not status:
                    return redirect(redirect_url)
                instance.proof_file = proof_file

            instance.save()

        messages.success(request,"Entry Updated Successfully!")
        return redirect(redirect_url)
    else:
        messages.error(request,'Method not allowed')
        return render(request, '404.html')