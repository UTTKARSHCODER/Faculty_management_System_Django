from datetime import datetime

from django.http.response import JsonResponse
from django.utils import timezone
import re
import firstWebsite.validations as va
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse

from firstWebsite.modals import Faculty, non_teaching_staff, Faculty_participation_data, mooc_course, events, \
    awards_and_achievments, sponsored_research, research_journal, research_conference, research_book, patents, guided, \
    resource
from firstWebsite.views import session_login_required


@session_login_required
def save_all_forms(request, pk):
    if pk:
        if request.method == 'POST':

            session = request.POST.get('sessionyear')
            faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))

            if pk == 16:
                # Profile Picture input can also be added on later discussion
                name = request.POST.get('name').strip()
                if not va.nameValidate(request,name,"Name"):
                    return redirect('all_forms',pk=pk)

                mobile_no = request.POST.get('mobile_no').strip()
                if not va.mobileNumberValidate(request,mobile_no):
                    return redirect('all_forms',pk=pk)

                department = request.POST.get('department',"").strip()

                lab_no = int(request.POST.get('lab_no') or 0)
                if not va.numberValidate(request,lab_no,"Lab Number"):
                    return redirect('all_forms', pk=pk)

                designation = request.POST.get('designation').strip()
                if not va.nameValidate(request,designation,"Designation"):
                    return redirect('all_forms', pk=pk)

                emp_id = int(request.POST.get('emp_id') or 0)
                if not va.numberValidate(request, emp_id, "Employee ID"):
                    return redirect('all_forms', pk=pk)

                highest_qual = request.POST.get('highest_qualification').strip()
                if not va.nameValidate(request,highest_qual,"Highest Qualification"):
                    return redirect('all_forms', pk=pk)

                university_name = request.POST.get('univ_name').strip()
                if not va.nameValidate(request,university_name,"University Name"):
                    return redirect('all_forms', pk=pk)

                pshd = int(request.POST.get('pshd') or 0)
                if not va.numberValidate(request,pshd,"Passing Year of Highest Degree"):
                    return redirect('all_forms', pk=pk)

                professional_course = request.POST.getlist('optradio').strip()
                if not va.radiocheck(request,professional_course,"Professional Course"):
                    return redirect('all_forms',pk=pk)

                pan_no = request.POST.get('pan_no').strip()
                if not va.validate_pan(pan_no) or not pan_no:
                    messages.error(request, "Please enter a valid PAN number")
                    return redirect('all_forms', pk=pk)

                dob = request.POST.get('dob')
                try:
                    selected_date = datetime.strptime(dob,'%Y-%m-%d').date()

                    max_date = datetime.strptime('2001-12-31', '%Y-%m-%d').date()
                    min_date = datetime.strptime('1930-01-01','%Y-%m-%d').date()

                    if not min_date < selected_date < max_date:
                        messages.error(request,f"Please select/enter date of birth in range of 1930-01-01 to 2001-12-31.You selected {selected_date}")
                        return redirect('all_forms',pk=pk)

                except(ValueError, TypeError):
                    messages.error(request,"Please select/enter a valid date of birth.")
                    return redirect('all_forms', pk=pk)

                joining_date = request.POST.get('jd')
                try:
                    selected_date = datetime.strptime(joining_date,'%Y-%m-%d').date()

                    min_date = datetime.strptime('2000-01-01','%Y-%m-%d').date()

                    if selected_date < min_date:
                        messages.error(request,"Please select/enter date greater than 2000-01-01")
                        return redirect('all_forms',pk=pk)

                except(ValueError, TypeError):
                    messages.error(request,"Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                promotion_date = request.POST.get('pd')
                if promotion_date == '':
                    promotion_date = None

                if request.FILES.get('jr'):
                    joining_report = request.FILES['jr']
                    if not va.fileValidate(request,joining_report,"Joining Report"):
                        return redirect('all_forms', pk=pk)

                if request.FILES.get('ol'):
                    offer_letter = request.FILES['jr']
                    if not va.fileValidate(request,offer_letter,"Offer Letter"):
                        return redirect('all_forms', pk=pk)

                if request.FILES.get('hdc'):
                    higher_degree_certificate = request.FILES['hdc']
                    if not va.fileValidate(request,higher_degree_certificate,"Higher Degree Certificate"):
                        return redirect('all_forms', pk=pk)

                if request.FILES.get('ss'):
                    salary_slip = request.FILES['ss']
                    if not va.fileValidate(request,salary_slip,"Salary Slip"):
                        return redirect('all_forms', pk=pk)

                if request.FILES.get('awards'):
                    certificate = request.FILES['awards']
                    if not va.fileValidate(request,certificate,"Co-curricular Certificate"):
                        return redirect('all_forms', pk=pk)

                obj = non_teaching_staff(name=name, mobile_no=mobile_no, email=faculty_instance, department=department, Lab_no=lab_no, designation=designation, emp_id=emp_id, highest_qual=highest_qual, university_name=university_name, pshd=pshd, professional_course=professional_course, pan_no=pan_no,dob=dob, joining_date=joining_date, promotion_date=promotion_date, joining_report=joining_report, offer_letter=offer_letter, higher_degree_certificate=higher_degree_certificate, salary_slip=salary_slip, certificate=certificate)
                obj.save()

            elif pk == 1:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms', pk=pk)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request,top,"Title of program"):
                    return redirect('all_forms', pk=pk)

                mode = request.POST.get('optradio').strip()
                if not va.radiocheck(request,mode,"mode"):
                    return redirect('all_forms', pk=pk)

                level = request.POST.get('optradio1').strip()
                if not va.radiocheck(request,level,"level"):
                    return redirect('all_forms', pk=pk)

                organizer = request.POST.get('organizer').strip()
                if not va.nameValidate(request,organizer,"Organizer"):
                    return redirect('all_forms', pk=pk)

                sponser = request.POST.get('sponser').strip()
                if not va.nameValidate(request,sponser,"Sponser"):
                    return redirect('all_forms', pk=pk)

                approval = request.POST.get('optradio2').strip()
                if not va.radiocheck(request,approval,"(SKIT approved)"):
                    return redirect('all_forms', pk=pk)

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)
                    begi_date = selected_date

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)
                    end_date = selected_date

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                num_of_days = (end_date - begi_date).days

                proof_approval = request.POST.get('optradio3').strip()
                if not va.radiocheck(request,proof_approval,"Proof Approval"):
                    return redirect('all_forms',pk=pk)

                if request.FILES.get('proof_file'):
                    proof_file_path = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file_path,"Proof File"):
                        return redirect('all_forms', pk=pk)

                obj1 = Faculty_participation_data(category=category,top=top,mode=mode,level=level,organizer=organizer,sponsors=sponser,approval=approval,begi_date=begi_date,end_date=end_date,session=session,no_of_days=num_of_days,proof_enclosed=proof_approval,proof_file=proof_file_path,email=faculty_instance)
                obj1.save()

            elif pk == 2:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=pk)

                timeline = request.POST.get('toc').strip()
                if not va.nameValidate(request,category,"Timeline of Course"):
                    return redirect('all_forms',pk=pk)

                noc = request.POST.get('noc').strip()
                if not va.nameValidate(request,category,"Name of Course"):
                    return redirect('all_forms',pk=pk)

                doc = request.POST.get('optradio3').strip()
                if not va.nameValidate(request,category,"Duration of Course"):
                    return redirect('all_forms',pk=pk)

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                offer = request.POST.get('ofo').strip()
                if not va.nameValidate(request, category, "Offering Agency/ Organizer"):
                    return redirect('all_forms', pk=pk)

                ctype = request.POST.get('optradio1').strip()
                if not va.radiocheck(request, category, "Certificate Type"):
                    return redirect('all_forms', pk=pk)

                topper_in = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, category, "Topper Category"):
                    return redirect('all_forms', pk=pk)

                remarks = request.POST.get('remarks').strip()

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file,"Proof File"):
                        return redirect('all_forms',pk=pk)

                obj2 = mooc_course(category=category,timeline=timeline,noc=noc,doc=doc,begi_date=begi_date,end_date=end_date,offer=offer,ctype=ctype,topper_in=topper_in,session=session,remarks=remarks,proof_file=proof_file,email=faculty_instance)
                obj2.save()

            elif pk == 3:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=pk)

                eof = request.POST.get('optradio3').strip()
                if not va.radiocheck(request,eof,"Event organized for"):
                    return redirect('all_forms',pk=pk)

                nofc = request.POST.get('nofc').strip()
                if not va.nameValidate(request,nofc,"Name of Faculty Coordinator(s)"):
                    return redirect('all_forms',pk=pk)

                topdpo = request.POST.get('topdpo').strip()
                if not va.nameValidate(request,topdpo,"Title of Professional Development Program Organized"):
                    return redirect('all_forms',pk=pk)

                nop = int(request.POST.get('nop') or 0)
                if not va.numberValidate(request,nop,"Number of participants"):
                    return redirect('all_forms',pk=pk)

                adcc = request.POST.get('adcc').strip()
                if not va.nameValidate(request,adcc,"Academic Department"):
                    return redirect('all_forms',pk=pk)

                ct = request.POST.get('optradio1').strip()
                if not va.radiocheck(request,ct,"Certificate Type"):
                    return redirect('all_forms',pk=pk)

                nosa = request.POST.get('nosa').strip()
                if not va.nameValidate(request,nosa,"Name of Sponsoring Agency"):
                    return redirect('all_forms',pk=pk)

                cd = request.POST.get('cd').strip()
                if not va.nameValidate(request,cd,"Collaboration Details"):
                    return redirect('all_forms',pk=pk)

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                gr = request.POST.get('optradio2').strip()
                if not va.radiocheck(request,gr,"Grant Recieved"):
                    return redirect('all_forms',pk=pk)

                gd = request.POST.get('gd').strip()
                if not va.nameValidate(request,gd,"Grant Details"):
                    return redirect('all_forms',pk=pk)

                awpsfooe = request.POST.get('awpsfooe').strip()
                if not va.nameValidate(request,gr,"Association with professional societies for organization of event"):
                    return redirect('all_forms',pk=pk)

                nossp = int(request.POST.get('nossp') or 0)
                if not va.numberValidate(request,gr,"Number of SKIT students participated"):
                    return redirect('all_forms',pk=pk)

                nosmp = int(request.POST.get('nosmp') or 0)
                if not va.numberValidate(request,nosmp,"Number of staff member participated"):
                    return redirect('all_forms', pk=pk)

                eraipf = request.POST.get('optradio4').strip()
                if not va.radiocheck(request,eraipf,"Event Report attached(Yes/No)"):
                    return redirect('all_fomrs',pk=pk)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file,"Proof file"):
                        return redirect('all_forms',pk=pk)

                remarks = request.POST.get('remarks')

                obj3 = events(category=category,eof=eof,nofc=nofc,topdpo=topdpo,nop=nop,adcc=adcc,session=session,ct=ct,nosa=nosa,cd=cd,begi_date=begi_date,end_date=end_date,gr=gr,gd=gd,awpsfooe=awpsfooe,nossp=nossp,nosmp=nosmp,eraipf=eraipf,proof_file=proof_file,remarks=remarks,email=faculty_instance)
                obj3.save()

            elif pk == 4:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=pk)

                noaa = request.POST.get('noaa').strip()
                if not va.nameValidate(request,noaa,"Name of award/Achievement"):
                    return redirect('all_forms',pk=pk)

                paf = request.POST.get('paf').strip()
                if not va.alphanumnameValidate(request, noaa, "Position / Award For"):
                    return redirect('all_forms', pk=pk)

                ao = request.POST.get('ao').strip()
                if not va.nameValidate(request, noaa, "Agency / Organization"):
                    return redirect('all_forms', pk=pk)

                prize = request.POST.get('prize').strip()
                if not va.alphanumnameValidate(request, noaa, "Prize"):
                    return redirect('all_forms', pk=pk)

                ad = request.POST.get('award_date')
                try:
                    selected_date = datetime.strptime(ad, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                remark = request.POST.get('remark').strip()

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file,"Proof File"):
                        return redirect('all_forms',pk=pk)

                obj4 = awards_and_achievments(category=category,noaa=noaa,paf=paf,ao=ao,prize=prize,ad=ad,remark=remark,session=session,proof_file=proof_file,email=faculty_instance)
                obj4.save()

            elif pk == 5:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=pk)

                nofa = request.POST.get('nofa').strip()
                if not va.nameValidate(request, nofa, "Name of Funding Agency"):
                    return redirect('all_forms', pk=pk)

                dop = str(request.POST.get('dop'))
                if not va.nameValidate(request,dop,"Duration of project"):
                    return redirect('all_forms',pk=pk)

                amount = int(request.POST.get('amount') or 0)
                if not va.numberValidate(request,amount,"Amount"):
                    return redirect('all_forms',pk=pk)

                status = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, dop, "Status"):
                    return redirect('all_forms', pk=pk)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request,proof_file,"Proof File"):
                        return redirect('all_forms',pk=pk)

                obj5 = sponsored_research(category=category,nofa=nofa,dop=dop,amount=amount,session=session,status=status,proof_file=proof_file,email=faculty_instance)
                obj5.save()

            elif pk == 6:
                noa = request.POST.get('noa').strip()
                if not va.nameValidate(request,noa,"Name of the author(s)"):
                    return redirect('all_forms',pk=pk)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request,top,"Title of paper"):
                    return redirect('all_forms',pk=pk)

                noj = request.POST.get('noj').strip()
                if not va.nameValidate(request,noj,"Name of Journal"):
                    return redirect('all_forms',pk=pk)

                nop = request.POST.get('nop').strip()
                if not va.nameValidate(request,nop,"Name of the Publisher"):
                    return redirect('all_forms',pk=pk)

                vi = int(request.POST.get('vi') or 0)
                if not va.numberValidate(request,vi,"Volumne, Issue"):
                    return redirect('all_forms',pk=pk)

                pn = int(request.POST.get('pn') or 0)
                if not va.numberValidate(request,pn,"Page Number"):
                    return redirect('all_forms',pk=pk)

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                isnp = request.POST.get('isnp').strip()
                if not va.alphanumnameValidate(request, pn, "ISSN number : Print"):
                    return redirect('all_forms', pk=pk)

                isno = request.POST.get('isno').strip()
                if not va.alphanumnameValidate(request, pn, "ISSN number : Online"):
                    return redirect('all_forms', pk=pk)

                level = request.POST.get('optradio3').strip()
                if not va.nameValidate(request, pn, "Level (National/ International)"):
                    return redirect('all_forms', pk=pk)

                doi = request.POST.get('doi').strip()
                if not va.alphanumnameValidate(request, pn, "DOI(Digital Object Identifier)"):
                    return redirect('all_forms', pk=pk)

                lwj = request.POST.get('lwj').strip()
                if not va.nameValidate(request, pn, "Link to website of the Journal"):
                    return redirect('all_forms', pk=pk)

                lap = request.POST.get('lap').strip()
                if not va.nameValidate(request, pn, "Link to article/paper/ abstract of the article"):
                    return redirect('all_forms', pk=pk)

                lrsj = request.POST.get('lrsj').strip()
                if not va.nameValidate(request, pn, "Link to the recognition in SCOPUS enlistment of the Journal"):
                    return redirect('all_forms', pk=pk)

                aiop = request.POST.get('aiop').strip()
                if not va.nameValidate(request, pn, "Affiliating Institute at the time of publication"):
                    return redirect('all_forms', pk=pk)

                ssa = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, pn, "Is SKIT student associated"):
                    return redirect('all_forms', pk=pk)

                details = request.POST.get('details').strip()
                if not va.nameValidate(request, pn, "If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)"):
                    return redirect('all_forms', pk=pk)

                index_by = request.POST.get('optradio1').strip()
                if not va.radiocheck(request, pn, "Indexed by"):
                    return redirect('all_forms', pk=pk)

                quartile = request.POST.get('optradio').strip()
                if not va.radiocheck(request, pn, "Quartile"):
                    return redirect('all_forms', pk=pk)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', pk=pk)

                obj6 = research_journal(noa=noa,top=top,noj=noj,nop=nop,vi=vi,pn=pn,pd=pd,session=session,isnp=isnp,isno=isno,level=level,doi=doi,lwj=lwj,lap=lap,lrsj=lrsj,aiop=aiop,ssa=ssa,details=details,index_by=index_by,quartile=quartile,proof_file=proof_file,email=faculty_instance)
                obj6.save()

            elif pk == 7:
                noa = request.POST.get('noa').strip()
                if not va.nameValidate(request, noa, "Name of the author(s)"):
                    return redirect('all_forms', pk=pk)

                toc = request.POST.get('toc').strip()
                if not va.nameValidate(request, toc, "Title of Conference"):
                    return redirect('all_forms', pk=pk)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request, top, "Title of Paper"):
                    return redirect('all_forms', pk=pk)

                topc = request.POST.get('topc').strip()
                if not va.nameValidate(request, topc, "Title of the proceedings of the conference"):
                    return redirect('all_forms', pk=pk)

                level = request.POST.get('optradio3').strip()
                if not va.nameValidate(request, level, "Level (National/ International)"):
                    return redirect('all_forms', pk=pk)

                isnp = request.POST.get('isnp').strip()
                if not va.nameValidate(request, isnp, "ISBN/ISSN number of the proceeding"):
                    return redirect('all_forms', pk=pk)

                nop = request.POST.get('nop').strip()
                if not va.nameValidate(request, nop, "Name of the Publisher"):
                    return redirect('all_forms', pk=pk)

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                doi = request.POST.get('doi').strip()
                if not va.nameValidate(request, doi, "DOI(Digital Object Identifier)"):
                    return redirect('all_forms', pk=pk)

                lwj = request.POST.get('lwj').strip()
                if not va.nameValidate(request, lwj, "Link to website of the Journal"):
                    return redirect('all_forms', pk=pk)

                aitp = request.POST.get('aitp').strip()
                if not va.nameValidate(request, aitp, "Affiliating Institute at the time of publication"):
                    return redirect('all_forms', pk=pk)

                ssa = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, ssa, "Is SKIT student associated"):
                    return redirect('all_forms', pk=pk)

                details = request.POST.get('details').strip()
                if not va.nameValidate(request, details, "If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)"):
                    return redirect('all_forms', pk=pk)

                index_by = request.POST.get('optradio1').strip()
                if not va.radiocheck(request, index_by, "Indexed by"):
                    return redirect('all_forms', pk=pk)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', pk=pk)

                obj7 = research_conference(noa=noa,toc=toc,top=top,topc=topc,level=level,isnp=isnp,nop=nop,pd=pd,session=session,doi=doi,lwj=lwj,aitp=aitp,ssa=ssa,details=details,index_by=index_by,proof_file=proof_file,email=faculty_instance)
                obj7.save()

            elif pk == 8:
                noa = request.POST.get('noa').strip()
                if not va.nameValidate(request, noa, "Name of the author(s)"):
                    return redirect('all_forms', pk=pk)

                tob = request.POST.get('tob').strip()
                if not va.nameValidate(request, tob, "Title of the book"):
                    return redirect('all_forms', pk=pk)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request, top, "Title of the chapter Published"):
                    return redirect('all_forms', pk=pk)

                level = request.POST.get('optradio3').strip()
                if not va.radiocheck(request, level, "Level (National/ International)"):
                    return redirect('all_forms', pk=pk)

                isbn = request.POST.get('isbn').strip()
                if not va.nameValidate(request, isbn, "ISBN"):
                    return redirect('all_forms', pk=pk)

                nop = request.POST.get('nop').strip()
                if not va.nameValidate(request, nop, "Name of the Publisher"):
                    return redirect('all_forms', pk=pk)

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                doi = request.POST.get('doi').strip()
                if not va.nameValidate(request, doi, "DOI(Digital Object Identifier)"):
                    return redirect('all_forms', pk=pk)

                lwj = request.POST.get('lwj').strip()
                if not va.nameValidate(request, lwj, "Link to website of the Journal"):
                    return redirect('all_forms', pk=pk)

                aitp = request.POST.get('aitp').strip()
                if not va.nameValidate(request, aitp, "Affiliating Institute at the time of publication"):
                    return redirect('all_forms', pk=pk)

                ssa = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, ssa, "Is SKIT student associated"):
                    return redirect('all_forms', pk=pk)

                details = request.POST.get('details').strip()
                if not va.nameValidate(request, details, "Write student(s) details"):
                    return redirect('all_forms', pk=pk)

                index_by = request.POST.get('optradio1').strip()
                if not va.radiocheck(request, index_by, "Indexed by"):
                    return redirect('all_forms', pk=pk)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', pk=pk)

                obj8 = research_book(noa=noa,tob=tob,top=top,level=level,isbn=isbn,nop=nop,pd=pd,session=session,doi=doi,lwj=lwj,aitp=aitp,ssa=ssa,details=details,index_by=index_by,proof_file=proof_file,email=faculty_instance)
                obj8.save()

            elif pk == 9:
                sop = request.POST.get('optradio1').strip()
                if not va.radiocheck(request, sop, "Status of Patent"):
                    return redirect('all_forms', pk=pk)

                gi = request.POST.get('nof').strip()
                if not va.alphanumnameValidate(request, gi, "Granted ID"):
                    return redirect('all_forms', pk=pk)

                ag = request.POST.get('ag').strip()
                if not va.alphanumnameValidate(request, ag, "Application ID"):
                    return redirect('all_forms', pk=pk)

                top = request.POST.get('top').strip()
                if not va.nameValidate(request, top, "Title of Patent"):
                    return redirect('all_forms', pk=pk)

                gc = request.POST.get('gc').strip()
                if not va.nameValidate(request, gc, "Granted Country"):
                    return redirect('all_forms', pk=pk)

                pfd = request.POST.get('filed_date')
                try:
                    selected_date = datetime.strptime(pfd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                pd = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(pd, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                pg = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, pg, "Type of Patent"):
                    return redirect('all_forms', pk=pk)

                ssa = request.POST.get('optradio').strip()
                if not va.radiocheck(request, ssa, "Is SKIT student associated"):
                    return redirect('all_forms', pk=pk)

                details = request.POST.get('details').strip()
                if not va.nameValidate(request, details, "Write student(s) details"):
                    return redirect('all_forms', pk=pk)

                link = request.POST.get('link').strip()

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', pk=pk)

                obj9 = patents(sop=sop,gi=gi, ag=ag, top=top, gc=gc,pfd=pfd, pd=pd, session=session, pg=pg, ssa=ssa, details=details, link=link, proof_file=proof_file,email=faculty_instance)
                obj9.save()

            elif pk == 10:
                nos = request.POST.get('nos').strip()
                if not va.nameValidate(request, nos, "Name of the student Guided"):
                    return redirect('all_forms', pk=pk)

                ens = request.POST.get('ens').strip()
                if not va.alphanumnameValidate(request, ens, "Enrollment Number of Student"):
                    return redirect('all_forms', pk=pk)

                urns = request.POST.get('urns').strip()
                if not va.alphanumnameValidate(request, urns, "University Roll Number of Student"):
                    return redirect('all_forms', pk=pk)

                eys = request.POST.get('enrollmentyear').strip()
                if not va.nameValidate(request, eys, "Enrollment Year of Student"):
                    return redirect('all_forms', pk=pk)

                tod = request.POST.get('tod').strip()
                if not va.nameValidate(request, tod, "Title of the Dissertation"):
                    return redirect('all_forms', pk=pk)

                visor = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, visor, "Supervisor / Co-supervisor"):
                    return redirect('all_forms', pk=pk)

                dov = request.POST.get('dov')
                try:
                    selected_date = datetime.strptime(dov, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                noe = request.POST.get('noe').strip()
                if not va.nameValidate(request, noe, "Name of external examiner"):
                    return redirect('all_forms', pk=pk)

                obj10 = guided(nos=nos, ens=ens, urns=urns, eys=eys, tod=tod, visor=visor, dov=dov, noe=noe, session=session,email=faculty_instance)
                obj10.save()

            elif pk == 11:
                category = request.POST.get('category').strip()
                if not va.nameValidate(request,category,"Category"):
                    return redirect('all_forms',pk=pk)

                toe = request.POST.get('toe').strip()
                if not va.nameValidate(request, toe, "Title of Event/ Exam Name"):
                    return redirect('all_forms', pk=pk)

                sa = request.POST.get('sa').strip()
                if not va.nameValidate(request, sa, "Subject Area"):
                    return redirect('all_forms', pk=pk)

                doe = int(request.POST.get('doe') or 0)
                if not va.numberValidate(request, doe, "Duration of event (in days)"):
                    return redirect('all_forms', pk=pk)

                rpt = request.POST.get('optradio2').strip()
                if not va.radiocheck(request, rpt, "Resource Person Type"):
                    return redirect('all_forms', pk=pk)

                begi_date = request.POST.get('begi_date')
                try:
                    selected_date = datetime.strptime(begi_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                end_date = request.POST.get('end_date')
                try:
                    selected_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                    if selected_date > timezone.now().date():
                        messages.error(request, "Date cannot be in future")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                venue = request.POST.get('venue').strip()
                if not va.nameValidate(request, venue, "Venue"):
                    return redirect('all_forms', pk=pk)

                if request.FILES.get('proof_file'):
                    proof_file = request.FILES['proof_file']
                    if not va.fileValidate(request, proof_file, "Proof File"):
                        return redirect('all_forms', pk=pk)

                obj11 = resource(category=category,toe=toe, sa=sa,doe=doe, rpt=rpt, begi_date=begi_date, end_date=end_date, session=session, venue=venue, proof_file=proof_file,email = faculty_instance)
                obj11.save()

            elif pk == 13:
                faculty_instance.name = request.POST.get('name').strip()
                if not va.nameValidate(request, faculty_instance.name, "Name"):
                    return redirect('all_forms', pk=pk)

                faculty_instance.contact_number = request.POST.get('mobile_no').strip()
                mobilepattern = r'[6789][0-9]{9}'
                if not re.match(mobilepattern, faculty_instance.contact_number):
                    messages.error(request,"Mobile number should start with 6,7,8,9 and should not conatain any alphabets or special characters.")
                    return redirect('all_forms', pk=pk)

                faculty_instance.email = request.POST.get('email').strip()

                faculty_instance.gender = request.POST.get('optradio').strip()
                if not va.radiocheck(request, faculty_instance.gender, "Gender"):
                    return redirect('all_forms', pk=pk)

                faculty_instance.department = request.POST.get('department').strip()

                faculty_instance.emp_id = int(request.POST.get('emp_id') or 0)
                if not va.numberValidate(request, faculty_instance.emp_id, "Employee ID"):
                    return redirect('all_forms', pk=pk)

                faculty_instance.designation = request.POST.get('designation').strip()

                faculty_instance.aos = request.POST.get('aos').strip()
                if not va.radiocheck(request, faculty_instance.aos, "Area of Specialization"):
                    return redirect('all_forms', pk=pk)

                faculty_instance.hq = request.POST.get('highest_qualification').strip()
                if not va.radiocheck(request, faculty_instance.hq, "Highest Qualification"):
                    return redirect('all_forms', pk=pk)

                faculty_instance.univ_name = request.POST.get('univ_name').strip()
                if not va.nameValidate(request, faculty_instance.univ_name, "University Name"):
                    return redirect('all_forms', pk=pk)

                faculty_instance.pshd = request.POST.get('pshd').strip()
                if not va.radiocheck(request, faculty_instance.pshd, "Passing Year of Highest Degree"):
                    return redirect('all_forms', pk=pk)

                faculty_instance.pan_no = request.POST.get('pan_no').strip()
                if not va.validate_pan(faculty_instance.pan_no) or not faculty_instance.pan_no:
                    messages.error(request, "Please enter a valid PAN number")
                    return redirect('all_forms', pk=pk)

                faculty_instance.dob = request.POST.get('dob')
                try:
                    selected_date = datetime.strptime(faculty_instance.dob, '%Y-%m-%d').date()

                    max_date = datetime.strptime('2001-12-31', '%Y-%m-%d').date()
                    min_date = datetime.strptime('1930-01-01', '%Y-%m-%d').date()

                    if not min_date < selected_date < max_date:
                        messages.error(request,
                                       f"Please select/enter date of birth in range of 1930-01-01 to 2001-12-31.You selected {selected_date}")
                        return redirect('all_forms', pk=pk)

                except(ValueError, TypeError):
                    messages.error(request, "Please select/enter a valid date of birth.")
                    return redirect('all_forms', pk=pk)

                faculty_instance.jd = request.POST.get('jd')
                try:
                    selected_date = datetime.strptime(faculty_instance.jd,'%Y-%m-%d').date()

                    min_date = datetime.strptime('2000-01-01','%Y-%m-%d').date()

                    if selected_date < min_date:
                        messages.error(request,"Please select/enter date greater than 2000-01-01")
                        return redirect('all_forms',pk=pk)

                except(ValueError, TypeError):
                    messages.error(request,"Please select/enter a valid date")
                    return redirect('all_forms', pk=pk)

                faculty_instance.pd = request.POST.get('pd')
                if faculty_instance.pd == '':
                    faculty_instance.pd = None
                else:
                    try:
                        selected_date = datetime.strptime(faculty_instance.pd, '%Y-%m-%d').date()

                        if selected_date > timezone.now().date():
                            messages.error(request, "Date cannot be in future")
                            return redirect('all_forms', pk=pk)

                    except(ValueError, TypeError):
                        messages.error(request, "Please select/enter a valid date")
                        return redirect('all_forms', pk=pk)

                faculty_instance.address = request.POST.get('address').strip()
                if not va.addressValidate(request, faculty_instance.address, "Address"):
                    return redirect('all_forms', pk=pk)

                if request.FILES.get('profile_picture'):
                    faculty_instance.profile_picture = request.FILES.get('profile_picture')
                    if not va.imageFileValidate(request, faculty_instance.profile_picture, "Profile Picture"):
                        return redirect('all_forms', pk=pk)

                if request.FILES.get('jr'):
                    faculty_instance.jr = request.FILES.get('jr')
                    if not va.fileValidate(request, faculty_instance.jr, "Joining Report"):
                        return redirect('all_forms', pk=pk)

                if request.FILES.get('ol'):
                    faculty_instance.of = request.FILES.get('ol')
                    if not va.fileValidate(request, faculty_instance.of, "Offer Letter"):
                        return redirect('all_forms', pk=pk)

                if request.FILES.get('hdc'):
                    faculty_instance.hdc = request.FILES.get('hdc')
                    if not va.fileValidate(request, faculty_instance.hdc, "Higher Degree Certificate"):
                        return redirect('all_forms', pk=pk)

                if request.FILES.get('ss'):
                    faculty_instance.ss = request.FILES.get('ss')
                    if not va.fileValidate(request, faculty_instance.ss, "Salary Slip"):
                        return redirect('all_forms', pk=pk)

                if request.FILES.get('awards'):
                    faculty_instance.certificate = request.FILES.get('awards')
                    if not va.fileValidate(request, faculty_instance.certificate, "Co-curricular Certificate"):
                        return redirect('all_forms', pk=pk)

                faculty_instance.phd_univ = request.POST.get('phd_univ').strip()
                if not va.nameValidate(request, faculty_instance.phd_univ, "PHD University Name"):
                    return redirect('all_forms', pk=pk)

                phd_dor = request.POST.get('phd_dor')
                if phd_dor == '':
                    faculty_instance.phd_dor = None
                else:
                    try:
                        selected_date = datetime.strptime(faculty_instance.pd, '%Y-%m-%d').date()

                        if selected_date > timezone.now().date():
                            messages.error(request, "Date cannot be in future")
                            return redirect('all_forms', pk=pk)

                    except(ValueError, TypeError):
                        messages.error(request, "Please select/enter a valid date")
                        return redirect('all_forms', pk=pk)

                faculty_instance.norp = int(request.POST.get('norp') or 0)
                if not va.numberValidate(request, faculty_instance.norp, "Number of Research Paper"):
                    return redirect('all_forms', pk=pk)
                faculty_instance.status = "R"

                faculty_instance.save()

            elif pk == 14:

                faculty_instance = Faculty.objects.get(email=request.POST.get('existing_email'))

                faculty_instance.name = request.POST.get('updated_name').strip()
                if not va.nameValidate(request, faculty_instance.name, "Name"):
                    return redirect(reverse('directory'))

                faculty_instance.contact_number = request.POST.get('updated_number').strip()
                if not va.mobileNumberValidate(request, faculty_instance.contact_number):
                    return redirect(reverse('directory'))

                faculty_instance.email = request.POST.get('updated_email').strip()
                if not va.emailValidate(request,faculty_instance.email):
                    return redirect(reverse('directory'))

                faculty_instance.department = request.POST.get('updated_department').strip()

                faculty_instance.role = request.POST.get('updated_role').strip()

                faculty_instance.emp_id = int(request.POST.get('updated_id') or 0)
                if not va.numberValidate(request, faculty_instance.name, "Employee ID"):
                    return redirect(reverse('directory'))

                faculty_instance.status = request.POST.get('updated_status').strip()

                faculty_instance.save()
                return redirect(reverse('directory'))

            elif pk == 15:
                emp_id = int(request.POST.get('emp_id') or 0)
                if not va.numberValidate(request, emp_id, "Employee ID"):
                    return redirect(reverse('directory'))

                emp_name = request.POST.get('name_per').strip()
                if not va.nameValidate(request, emp_id, "Name"):
                    return redirect(reverse('directory'))

                email = request.POST.get('new_email').strip()
                if not va.emailValidate(request, email):
                    return redirect(reverse('directory'))

                department = request.POST.get('selected_department').strip()

                role = request.POST.get('selected_role').strip()

                con_no = request.POST.get('contact_number').strip()
                if not va.mobileNumberValidate(request, emp_id):
                    return redirect(reverse('directory'))

                status = request.POST.get('selected_status').strip()

                obj12 = Faculty(name=emp_name,emp_id=emp_id,email=email,department=department,role=role,contact_number=con_no,status=status)
                obj12.save()

                return redirect(reverse('directory'))

            return JsonResponse({'status': 'success'})
        # Method not allowed
        return render(request, '404.html')

    return render(request,'404.html')