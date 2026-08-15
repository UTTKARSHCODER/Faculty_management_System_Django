import json
import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count

from MyFirstDjangoWebsite import settings
from firstWebsite.modals import Faculty, awards_and_achievments, category as cat, events, Faculty_participation_data, \
    guided, mooc_course, patents, research_book, research_conference, research_journal, resource, sponsored_research, \
    non_teaching_staff, department, index_by, level, type_of_patent
from firstWebsite.views import session_login_required
import jwt


@session_login_required
def progress_bar(request):
    try:
        faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))

        label_map = {choice.value: choice.label for choice in cat}

        non_teaching_instance = non_teaching_staff.objects.filter(email=faculty_instance).count()

        no_of_awards = list(awards_and_achievments.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in no_of_awards:
            item['category_display'] = label_map.get(item['category'], item['category'])

        events_instance = list(events.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in events_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        faculty_participartion_data = list(Faculty_participation_data.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in faculty_participartion_data:
            item['category_display'] = label_map.get(item['category'], item['category'])

        guided_instance = list(guided.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in guided_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        mooc_course_instance = list(mooc_course.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in mooc_course_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        patents_instance = patents.objects.filter(email=faculty_instance).count()

        research_book_instance = research_book.objects.filter(email=faculty_instance).count()

        research_conference_instance = research_conference.objects.filter(email=faculty_instance).count()

        research_journal_instance = research_journal.objects.filter(email=faculty_instance).count()

        resource_instance = list(resource.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in resource_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        sponsored_research_instance = list(sponsored_research.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in sponsored_research_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        total_forms = sum(item['count'] for item in no_of_awards) + sum(item['count'] for item in events_instance) + sum(item['count'] for item in faculty_participartion_data) + sum(item['count'] for item in guided_instance) + sum(item['count'] for item in mooc_course_instance) + patents_instance + research_book_instance + research_conference_instance + research_journal_instance + sum(item['count'] for item in resource_instance) + sum(item['count'] for item in sponsored_research_instance)

        total_remaining_field_forms = 12 - ((1 if non_teaching_instance > 0 else 0) + (1 if len(no_of_awards) > 0 else 0) + (1 if len(events_instance) > 0 else 0) + (1 if len(faculty_participartion_data) > 0 else 0) + (1 if len(guided_instance) > 0 else 0) + (1 if len(mooc_course_instance) > 0 else 0) + (1 if patents_instance > 0 else 0) + (1 if research_book_instance > 0 else 0) + (1 if research_conference_instance > 0 else 0) + (1 if research_journal_instance > 0 else 0) + (1 if len(resource_instance) > 0 else 0) + (1 if len(sponsored_research_instance) > 0 else 0))

        form_wise_count = [sum(item['count'] for item in faculty_participartion_data), sum(item['count'] for item in mooc_course_instance), sum(item['count'] for item in events_instance), sum(item['count'] for item in no_of_awards), sum(item['count'] for item in sponsored_research_instance), research_journal_instance, research_conference_instance, research_book_instance, patents_instance, sum(item['count'] for item in guided_instance), sum(item['count'] for item in resource_instance)]

        context = {'total_forms': total_forms,'total_rff' : total_remaining_field_forms, 'fpd1': 1, 'ntspd1' : non_teaching_instance, 'faa1': no_of_awards, 'eod1': events_instance, 'fdp1': faculty_participartion_data, 'mp1': guided_instance, 'msc1' : mooc_course_instance, 'patents1': patents_instance, 'rpb1': research_book_instance, 'rpcp1': research_conference_instance, 'rpj1': research_journal_instance, 'rp1': resource_instance, 'sgc1': sponsored_research_instance,'form_wise_count' : form_wise_count}
        return render(request,'progresschart.html',context)
    except Faculty.DoesNotExist:
        error_message = f"User does not exist in database."
        messages.error(request,error_message)
        return render(request,'index.html')

@session_login_required
def forms_listing(request, form_type):

    faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))

    non_teaching_staff_instance = non_teaching_staff.objects

    no_of_awards = awards_and_achievments.objects

    events_instance = events.objects

    faculty_participation_data = Faculty_participation_data.objects

    mooc_course_instance = mooc_course.objects

    guided_instance = guided.objects

    patents_instance = patents.objects

    research_book_instance = research_book.objects

    research_conference_instance = research_conference.objects

    research_journal_instance = research_journal.objects

    sponsored_research_instance = sponsored_research.objects

    resource_instance = resource.objects

    label_map = {choice.value: choice.label for choice in cat}

    non_teaching_staff_instance = list(non_teaching_staff_instance.filter(email=faculty_instance).values('id','name', 'dob' ,'email__email'))
    for item in non_teaching_staff_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")

    no_of_awards = list(no_of_awards.filter(email=faculty_instance).values('category','noaa', 'ad', 'id'))
    for item in no_of_awards:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")
        item["category_display"] = label_map.get(item["category"], item["category"])

    events_instance = list(events_instance.filter(email=faculty_instance).values('category','topdpo', 'begi_date', 'id'))
    for item in events_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")
        item["category_display"] = label_map.get(item["category"], item["category"])

    faculty_participation_data = list(faculty_participation_data.filter(email=faculty_instance).values('category','top', 'begi_date', 'id'))
    for item in faculty_participation_data:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")
        item["category_display"] = label_map.get(item["category"], item["category"])

    guided_instance = list(guided_instance.filter(email=faculty_instance).values('category', 'nos', 'dov', 'id'))
    for item in guided_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")
        item["category_display"] = label_map.get(item["category"], item["category"])

    mooc_course_instance = list(mooc_course_instance.filter(email=faculty_instance).values('category', 'noc', 'begi_date','id'))
    for item in mooc_course_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")
        item["category_display"] = label_map.get(item["category"], item["category"])

    patents_instance = list(patents_instance.filter(email=faculty_instance).values('id','gc','pd','top'))
    for item in patents_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")

    research_book_instance = list(research_book_instance.filter(email=faculty_instance).values('id','noa','pd','tob'))
    for item in research_book_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")

    research_conference_instance = list(research_conference_instance.filter(email=faculty_instance).values('id','noa','pd','top'))
    for item in research_conference_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")

    research_journal_instance = list(research_journal_instance.filter(email=faculty_instance).values('id','noa','pd','noj'))
    for item in research_journal_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")

    resource_instance = list(resource_instance.filter(email=faculty_instance).values('category','toe','begi_date','id'))
    for item in resource_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")
        item["category_display"] = label_map.get(item["category"], item["category"])

    sponsored_research_instance = list(sponsored_research_instance.filter(email=faculty_instance).values('category','nofa','created_at','id'))
    for item in sponsored_research_instance:
        item["token"] = jwt.encode({"user_pk": item['id']}, settings.SECRET_KEY, algorithm="HS256")
        item["category_display"] = label_map.get(item["category"], item["category"])

    context = {'form_type': form_type ,'nts': non_teaching_staff_instance ,'faa1': no_of_awards, 'eod1': events_instance,
               'fdp1': faculty_participation_data, 'mp1': guided_instance, 'msc1': mooc_course_instance,
               'patents1': patents_instance, 'rpb1': research_book_instance,
               'rpcp1': research_conference_instance, 'rpj1': research_journal_instance,
               'rp1': resource_instance, 'sgc1': sponsored_research_instance}

    return render(request, 'form_listing.html', context)

@session_login_required
def report(request):
    if request.session.get('topLeftBar') == 'spa' or request.session.get('topLeftBar') == 'ad':
        faculty_member = Faculty.objects.get(pk=request.session.get('user_id'))

        department_map = {choice.value: choice.label for choice in department}
        label_map = {choice.value: choice.label for choice in cat}
        index_by_map = {choice.value: choice.label for choice in index_by}
        level_map = {choice.value: choice.label for choice in level}
        top_map = {choice.value: choice.label for choice in type_of_patent}

        if faculty_member.form_alloted[0] == '1_1':
            first_tab_data = list(Faculty.objects.filter(status="R").values('department').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category'] = item['department']
                item['category_display'] = department_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '1_2':

            first_tab_data = non_teaching_staff.objects.all().count()

        elif faculty_member.form_alloted[0] == '2':

            first_tab_data = list(
                Faculty_participation_data.objects.all().values('category').annotate(
                    count=Count('id')))
            for item in first_tab_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '3':

            first_tab_data = list(
                mooc_course.objects.all().values('category').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '4':

            first_tab_data = list(events.objects.all().values('category').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '5':
            first_tab_data = list(
                awards_and_achievments.objects.all().values('category').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '6':

            first_tab_data = list(
                sponsored_research.objects.all().values('category').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '7_1':

            first_tab_data = list(
                research_journal.objects.all().values('index_by').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category'] = item['index_by']
                item['category_display'] = index_by_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '7_2':

            first_tab_data = list(
                research_conference.objects.all().values('level').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category'] = item['level']
                item['category_display'] = level_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '7_3':

            first_tab_data = list(research_book.objects.all().values('level').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category'] = item['level']
                item['category_display'] = level_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '7_4':

            first_tab_data = list(patents.objects.all().values('pg').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category'] = item['pg']
                item['category_display'] = top_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '8':

            first_tab_data = list(guided.objects.all().values('category').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif faculty_member.form_alloted[0] == '9':

            first_tab_data = list(
                resource.objects.all().values('category').annotate(count=Count('id')))
            for item in first_tab_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        else:

            first_tab_data = "Not Defined"


        paired_form = list(zip(faculty_member.form_alloted, faculty_member.form_alloted_display_list))

        context = {'user': request.session.get('topLeftBar'),'form_to_show' : paired_form, 'fac_ins' : Faculty.objects.filter(status="R").all(),
                   # This data is sent for Chart rendering
                   'form_alloted_data_list' : faculty_member.form_alloted, 'first_tab_data': first_tab_data}

        return render(request, 'entire_report.html', context)
    else:
        return render(request, '404.html')

def return_data(instance , zipped_values):

    datatosend = []

    for i, values in enumerate(instance, start=1):
        values_list = {'S.No' : i}
        for col_name, col_val, col_field in zipped_values:

            row_val = values
            for step in col_val.split('.'):
                if values is None:
                    break
                row_val = getattr(row_val, step)

            if col_field == 'file':
                if row_val:
                    values_list[col_name] = row_val.url
                else:
                    values_list[col_name] = 'Not Uploaded Yet'

            elif col_field == 'method':
                if callable(row_val):
                    values_list[col_name] = row_val()
                else:
                    values_list[col_name] = row_val

            elif col_field == 'date':
                if isinstance(row_val, (datetime.date, datetime.datetime)):
                    values_list[col_name] = row_val.strftime('%Y-%m-%d')
                else:
                    values_list[col_name] = 'No Value'

            else:
                values_list[col_name] = row_val
        datatosend.append(values_list)

    return datatosend

def showdynamictable(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form_to_load = data.get('form_id')

        department_map = {choice.value: choice.label for choice in department}
        label_map = {choice.value: choice.label for choice in cat}
        index_by_map = {choice.value: choice.label for choice in index_by}
        level_map = {choice.value: choice.label for choice in level}
        top_map = {choice.value: choice.label for choice in type_of_patent}

        if form_to_load == '1_1':
            instance = Faculty.objects.filter(status="R").only('session','name','email','designation','department',
                        'contact_number','dob','gender','address','aos','hq',
                        'pshd','emp_id','pan_no','jd','profile_picture','jr','of','hdc','ss','pd','phd_univ',
                        'phd_dor','norp','certificate')

            col_vals = [('Edit','secure_token','text'),
                        ('Session', 'get_session_display', 'method'),
                        ('Name','name','text'),
                        ('Email','email','text'),
                        ('Designation','get_designation_display','method'),
                        ('Department','get_department_display','method'),
                        ('Contact Number','contact_number','text'),
                        ('DOB','dob','date'),
                        ('Gender','get_gender_display','method'),
                        ('Address','address','text'),
                        ('Area of Specialization','get_aos_display','method'),
                        ('Highest Qualfication','get_hq_display','method'),
                        ('Year of Passing','pshd','text'),
                        ('Employee ID','emp_id','text'),
                        ('PAN No.','pan_no','text'),
                        ('Date of Joining(College)','jd','date'),
                        ('Profile Photo(File)','profile_picture','file'),
                        ('Joining Report Letter(File)','jr','file'),
                        ('Offer Letter(File)','of','file'),
                        ('Highest Degree Certificate(File)','hdc','file'),
                        ('Salary Slip(File)','ss','file'),
                        ('Date of Promotion','pd','date'),
                        ('Name of PHD University(If pusuing)','phd_univ','date'),
                        ('Date of Registration(for PHD Course)','phd_dor','date'),
                        ('Number of Research Papers','norp','norp'),
                        ('Certificate(File)','certificate','file')
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(Faculty.objects.filter(status="R").values('department').annotate(count=Count('id')))
            for item in map_data:
                item['category'] = item['department']
                item['category_display'] = department_map.get(item['category'], item['category'])

        elif form_to_load == '1_2':
            instance = non_teaching_staff.objects.only('email__email','session','name','mobile_no','department',
                                                       'Lab_no','designation','emp_id','highest_qual','university_name',
                                                       'pshd','higher_degree_certificate','professional_course','pan_no',
                                                       'dob','joining_date','promotion_date','joining_report','offer_letter',
                                                       'salary_slip','certificate')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email', 'email.email', 'text'),
                        ('Session', 'get_session_display', 'method'),
                        ('Name', 'name', 'text'),
                        ('Mobile No.', 'mobile_no', 'text'),
                        ('Department', 'get_department_display', 'method'),
                        ('Lab No.', 'Lab_no', 'text'),
                        ('Designation', 'get_designation_display', 'method'),
                        ('Employee ID', 'emp_id', 'text'),
                        ('Highest Qualfication', 'get_highest_qual_display', 'method'),
                        ('University Name', 'university_name', 'text'),
                        ('Passing Year of Highest degree', 'pshd', 'text'),
                        ('Higher Degree Certificate(Date of award)(File)', 'higher_degree_certificate', 'file'),
                        ('Professional Courses', 'professional_display_list', 'method'),
                        ('PAN No.', 'pan_no', 'text'),
                        ('Date of Birth', 'dob', 'date'),
                        ('Joining Date(DD, MM, YYYY)', 'joining_date', 'date'),
                        ('Promotion Date(If any)', 'promotion_date', 'date'),
                        ('Joining Report(File)', 'joining_report', 'file'),
                        ('Offer Letter (Appointment Letter)(File)', 'offer_letter', 'file'),
                        ('Salary Slip (Recently)(File)', 'salary_slip', 'file'),
                        ('If Awards and recognition received for extension activities (Upload Certificate)(File)', 'certificate', 'file')
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(non_teaching_staff.objects.values('department').annotate(count=Count('id')))
            for item in map_data:
                item['category'] = item['department']
                item['category_display'] = department_map.get(item['category'], item['category'])

        elif form_to_load == '2':
            instance = Faculty_participation_data.objects.only('email__email', 'email__emp_id', 'email__department',
                                            'email__name', 'top', 'category', 'mode', 'level', 'organizer',
                                            'sponsors', 'approval', 'begi_date', 'end_date', 'session', 'no_of_days', 'proof_enclosed',
                                            'proof_file')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email', 'email.email', 'text'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Name of Faculty Member', 'email.name', 'text'),
                        ('Title Of Program', 'top', 'text'),
                        ('Conference/FDP/ Workshop/Seminar/ STTP', 'get_category_display', 'method'),
                        ('Mode', 'get_mode_display', 'method'),
                        ('Level', 'get_level_display', 'method'),
                        ('Organizer', 'organizer', 'text'),
                        ('Sponsored By', 'sponsors', 'text'),
                        ('Grant Recieved from SKIT (Yes/No)', 'get_approval_display', 'method'),
                        ('From Date', 'begi_date', 'date'),
                        ('To Date', 'end_date', 'date'),
                        ('Session', 'get_session_display', 'method'),
                        ('No. of Days', 'no_of_days', 'text'),
                        ('Proof Enclosed (Yes/No)', 'get_proof_enclosed_display', 'method'),
                        ('Uploaded Certificate/Proof(File)', 'proof_file', 'file')
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(
                Faculty_participation_data.objects.all().values('category').annotate(
                    count=Count('id')))
            for item in map_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif form_to_load == '3':
            instance = mooc_course.objects.only('email__email','session','email__name','email__emp_id',
                                                  'email__department','category','timeline','noc','doc','begi_date','end_date',
                                                  'offer','ctype','topper_in','remarks','proof_file')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Session', 'get_session_display', 'method'),
                        ('Name of Faculty Member', 'email.name', 'text'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Type of Course', 'get_category_display', 'method'),
                        ('Timeline of course', 'timeline', 'text'),
                        ('Name of the Course', 'noc', 'text'),
                        ('Duration of Course', 'get_doc_display', 'method'),
                        ('Start Date of Course', 'begi_date', 'date'),
                        ('End Date of Course', 'end_date', 'date'),
                        ('Offering Agency/ Organizer', 'offer', 'text'),
                        ('Certificate Type', 'get_ctype_display', 'method'),
                        ('Any category from below', 'get_topper_in_display', 'method'),
                        ('Remarks(if any)', 'remarks', 'text'),
                        ('Uploaded Certificate(File)', 'proof_file', 'file'),
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(
                mooc_course.objects.all().values('category').annotate(count=Count('id')))
            for item in map_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif form_to_load == '4':
            instance = events.objects.only('email__email','begi_date','end_date','eof','category',
                                           'nofc','topdpo','nop','adcc','session','ct','nosa','cd','gr','gd',
                                           'awpsfooe','nossp','nosmp','eraipf','remarks','proof_file')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Start Date of the Event', 'begi_date', 'date'),
                        ('End Date of the Event', 'end_date', 'date'),
                        ('Event organized for', 'eof_display_list', 'method'),
                        ('Type of Event', 'get_category_display', 'method'),
                        ('Name of Faculty Coordinator(s)', 'nofc', 'text'),
                        ('Title of the Professional Development Program Organized', 'topdpo', 'text'),
                        ('No. of participants', 'nop', 'text'),
                        ('Academic Department/ Cell / Committees/ Labs /COE', 'adcc', 'text'),
                        ('Academic Session', 'get_session_display', 'method'),
                        ('Sponsored/Non Sponsored', 'get_ct_display', 'method'),
                        ('Name of Sponsoring Agency(if Sponsored)', 'nosa', 'text'),
                        ('Collaboration Details', 'cd', 'text'),
                        ('Grant Received(Yes/No)', 'get_gr_display', 'method'),
                        ('Grant Details', 'gd', 'text'),
                        ('Association with professional societies for organization of event', 'awpsfooe', 'text'),
                        ('Number of SKIT students participated (Provide list of students with their RTU roll no. & Certificates)', 'nossp', 'text'),
                        ('Number of staff member participated (Provide list of staff members with  their EMPLOYEE ID & Certificates)', 'nosmp', 'text'),
                        ("Mapped SDG's", 'map_sdg_display_list', 'method'),
                        ('Event report attached in proper format(Yes/No)', 'get_eraipf_display', 'method'),
                        ('Any Other Remark', 'remarks', 'text'),
                        ('Upload Event Report(File)', 'proof_file', 'file'),
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(events.objects.all().values('category').annotate(count=Count('id')))
            for item in map_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif form_to_load == '5':
            instance = awards_and_achievments.objects.only('email__email','session','email__name','email__emp_id',
                                                           'email__designation','email__department','noaa','category','paf','ao','prize','ad','remark')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Session', 'get_session_display', 'method'),
                        ('Faculty Name', 'email.name', 'text'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Designation', 'email.get_designation_display', 'method'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Name of Award/Achievement', 'noaa', 'text'),
                        ('Category', 'get_category_display', 'method'),
                        ('Position / Award For', 'paf', 'text'),
                        ('Agency / Organization', 'ao', 'text'),
                        ('Prize', 'prize', 'text'),
                        ('Award Date', 'ad', 'date'),
                        ('Remark', 'remark', 'text'),
                        ('Upload Award Certificate/Proof(File)', 'proof_file', 'file'),
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(
                awards_and_achievments.objects.all().values('category').annotate(count=Count('id')))
            for item in map_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif form_to_load == '6':
            instance = sponsored_research.objects.only('email__email','email__name',
                                                         'email__emp_id','email__department','category','nofa','dop',
                                                         'amount','session','status','proof_file')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Name of Candidate (PI/Co PI)', 'email.name', 'text'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Category', 'get_category_display', 'method'),
                        ('Name of the Funding Agency(MSME/DST/CSIR/SERB /Industry etc.)', 'nofa', 'text'),
                        ('Duration of Project (in Years)', 'dop', 'text'),
                        ('Amount in Rs.', 'amount', 'text'),
                        ('Session', 'get_session_display', 'method'),
                        ('Status', 'get_status_display', 'method'),
                        ('Upload Proof(File)', 'proof_file', 'file'),
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(
                sponsored_research.objects.all().values('category').annotate(count=Count('id')))
            for item in map_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif form_to_load == '7_1':
            instance = research_journal.objects.only('email__email','email__emp_id','noa','email__department',
                                                     'top','noj','nop','vi','pn','pd','session','isnp','isno','level','doi',
                                                     'lwj','lap','lrsj','aiop','index_by','quartile','ssa','details','proof_file')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Name of the author(s)', 'noa', 'text'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Title of Paper', 'top', 'text'),
                        ('Name of Journal', 'noj', 'text'),
                        ('Name of the Publisher', 'nop', 'text'),
                        ('Volumne, Issue', 'vi', 'text'),
                        ('Page No.', 'pn', 'text'),
                        ('Published Date', 'pd', 'date'),
                        ('Session', 'get_session_display', 'method'),
                        ('ISSN number : Print', 'isnp', 'text'),
                        ('ISSN number : Online', 'isno', 'text'),
                        ('Level (National/ International)', 'get_level_display', 'method'),
                        ('DOI(Digital Object Identifier)', 'doi', 'text'),
                        ('Link to website of the Journal', 'lwj', 'text'),
                        ('Link to article/paper/abstract of the article (Direct link to the webpage where the abstract of paper is displayed)', 'lap', 'text'),
                        ('Link to the recognition in SCOPUS enlistment of the Journal', 'lrsj', 'text'),
                        ('Affiliating Institute at the time of publication', 'aiop', 'text'),
                        ('Indexed by', 'get_index_by_display', 'method'),
                        ('Quartile', 'get_quartile_display', 'method'),
                        ('Is SKIT student associated?', 'get_ssa_display', 'method'),
                        ('If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)', 'details', 'text'),
                        ('Upload Full Paper(File)', 'proof_file', 'file')
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(
                research_journal.objects.all().values('index_by').annotate(count=Count('id')))
            for item in map_data:
                item['category'] = item['index_by']
                item['category_display'] = index_by_map.get(item['category'], item['category'])

        elif form_to_load == '7_2':
            instance = research_conference.objects.only('email__email','email__department','email__emp_id',
                                                     'noa','toc','top','topc','level','isnp','nop','pd','session','doi','lwj',
                                                     'aitp','index_by','ssa','details','proof_file')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Name of the author(s)', 'noa', 'text'),
                        ('Title of Conference', 'toc', 'text'),
                        ('Title of Paper', 'top', 'text'),
                        ('Title of the proceedings of the conference', 'topc', 'text'),
                        ('Level (National/ International)', 'get_level_display', 'method'),
                        ('ISBN/ISSN number of the proceeding', 'isnp', 'text'),
                        ('Name of the Publisher', 'nop', 'text'),
                        ('Published Date', 'pd', 'date'),
                        ('Session', 'get_session_display', 'method'),
                        ('DOI(Digital Object Identifier)', 'doi', 'text'),
                        ('Web Link', 'lwj', 'text'),
                        ('Affiliating Institute at the time of publication', 'aitp', 'text'),
                        ('Indexed by', 'index_by', 'method'),
                        ('Is SKIT student associated?', 'get_ssa_display', 'method'),
                        ('If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)', 'details',
                         'text'),
                        ('Upload Full Paper(File)', 'proof_file', 'file')
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(
                research_conference.objects.all().values('level').annotate(count=Count('id')))
            for item in map_data:
                item['category'] = item['level']
                item['category_display'] = level_map.get(item['category'], item['category'])

        elif form_to_load == '7_3':
            instance = research_book.objects.only('email__email','email__department','email__emp_id','noa',
                                                  'tob','top','level','isbn','nop','pd','session','doi','lwj','aitp','index_by',
                                                  'ssa','details','proof_file')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Name of the author/editor', 'noa', 'text'),
                        ('Title of the book', 'tob', 'text'),
                        ('Title of the chapter Published', 'top', 'text'),
                        ('Level (National/ International)', 'get_level_display', 'method'),
                        ('ISBN', 'isbn', 'text'),
                        ('Name of the Publisher', 'nop', 'text'),
                        ('Published Date', 'pd', 'date'),
                        ('Session', 'get_session_display', 'method'),
                        ('DOI(Digital Object Identifier)', 'doi', 'text'),
                        ('Web Link', 'lwj', 'text'),
                        ('Affiliating Institute at the time of publication', 'aitp', 'text'),
                        ('Indexed by', 'index_by', 'method'),
                        ('Is SKIT student associated?', 'get_ssa_display', 'method'),
                        ('If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)', 'details',
                         'text'),
                        ('Upload Proof (Book Chapter/Front Page/Document etc.)(File)', 'proof_file', 'file')
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(research_book.objects.all().values('level').annotate(count=Count('id')))
            for item in map_data:
                item['category'] = item['level']
                item['category_display'] = level_map.get(item['category'], item['category'])

        elif form_to_load == '7_4':
            instance = patents.objects.only('email__email','session','email__department','email__emp_id','email__name',
                                            'sop','ag','gi','pg','top','gc','pfd','pd','ssa','details','link','proof_file')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Session', 'get_session_display', 'method'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Name of Faculty', 'email.name', 'text'),
                        ('Status of Patent', 'get_sop_display', 'method'),
                        ('Application ID', 'ag', 'text'),
                        ('Granted ID', 'gi', 'text'),
                        ('Type of Patent', 'get_pg_display', 'method'),
                        ('Title of Patent', 'top', 'text'),
                        ('Granted Country', 'gc', 'text'),
                        ('Patent Filed Date', 'pfd', 'date'),
                        ('Publication Date', 'pd', 'date'),
                        ('Is SKIT student associated?', 'get_ssa_display', 'method'),
                        ('If Yes , Write student(s) details (Program, Branch, RollNo/EnrollNo, Name)', 'details',
                         'text'),
                        ('Link', 'link', 'text'),
                        ('Upload Full Paper(File)', 'proof_file', 'file')
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(patents.objects.all().values('pg').annotate(count=Count('id')))
            for item in map_data:
                item['category'] = item['pg']
                item['category_display'] = top_map.get(item['category'], item['category'])

        elif form_to_load == '8':
            instance = guided.objects.only('email__email','session','email__name','email__emp_id',
                                           'email__department','nos','category','ens','urns','eys','tod','visor','dov','noe')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Session', 'get_session_display', 'method'),
                        ('Faculty Name', 'email.name', 'text'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Name of the student Guided', 'nos', 'text'),
                        ('Program of Student', 'get_category_display', 'method'),
                        ('Enrollment Number of Student', 'ens', 'text'),
                        ('University Roll Number of Student', 'urns', 'text'),
                        ('Enrollment Year of Student', 'get_eys_display', 'method'),
                        ('Title of the Dissertation', 'tod', 'text'),
                        ('Supervisor / Co-supervisor', 'get_visor_display', 'method'),
                        ('Date of Viva-Voce', 'dov', 'date'),
                        ('Name of external examiner', 'noe', 'text')
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(guided.objects.all().values('category').annotate(count=Count('id')))
            for item in map_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        elif form_to_load == '9':
            instance = resource.objects.only('email__email','session','email__name','email__emp_id','email__department',
                                             'category','toe','sa','rpt','doe','begi_date','end_date','venue','proof_file')

            col_vals = [('Edit', 'secure_token', 'text'),
                        ('Email address', 'email.email', 'text'),
                        ('Session', 'get_session_display', 'method'),
                        ('Name of Faculty Member', 'email.name', 'text'),
                        ('Employee ID', 'email.emp_id', 'text'),
                        ('Department', 'email.get_department_display', 'method'),
                        ('Resource Person in', 'get_category_display', 'method'),
                        ('Title of Event/ Exam Name ', 'toe', 'text'),
                        ('Subject Area/Subject Name/Lab Name/Session Name', 'sa', 'text'),
                        ('Resource Person Type', 'get_rpt_display', 'method'),
                        ('Duration of event (in days)', 'doe', 'text'),
                        ('From Date', 'begi_date', 'date'),
                        ('To Date', 'end_date', 'date'),
                        ('Venue', 'venue', 'text'),
                        ('Proof(Certificate/Mail)(File)', 'proof_file', 'file')
                        ]

            datatosend = return_data(instance, col_vals)

            map_data = list(
                resource.objects.all().values('category').annotate(count=Count('id')))
            for item in map_data:
                item['category_display'] = label_map.get(item['category'], item['category'])

        else:
            return JsonResponse({'success': False, 'message': 'Wrong Table entered'})

        return JsonResponse({'success' : True, 'row_values': datatosend, 'map_data' : map_data})
