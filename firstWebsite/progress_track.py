from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from firstWebsite.modals import Faculty, awards_and_achievments, category as cat, events, Faculty_participation_data, \
    guided, mooc_course, patents, research_book, research_conference, research_journal, resource, sponsored_research, \
    non_teaching_staff, department, index_by, level, type_of_patent
from firstWebsite.views import session_login_required


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
def forms_listing(request, pk):

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

    if pk == "filled_forms" or pk == "unfilled_forms" or pk == "all_forms":
        form_type = pk
        label_map = {choice.value: choice.label for choice in cat}

        non_teaching_staff_instance = list(non_teaching_staff_instance.filter(email=faculty_instance).values('id','name', 'dob' ,'email__email'))

        no_of_awards = list(no_of_awards.filter(email=faculty_instance).values('category','noaa', 'ad', 'id'))
        for item in no_of_awards:
            item["category_display"] = label_map.get(item["category"], item["category"])

        events_instance = list(events_instance.filter(email=faculty_instance).values('category','topdpo', 'begi_date', 'id'))
        for item in events_instance:
            item["category_display"] = label_map.get(item["category"], item["category"])

        faculty_participation_data = list(faculty_participation_data.filter(email=faculty_instance).values('category','top', 'begi_date', 'id'))
        for item in faculty_participation_data:
            item["category_display"] = label_map.get(item["category"], item["category"])

        guided_instance = list(guided_instance.filter(email=faculty_instance).values('category', 'nos', 'dov', 'id'))
        for item in guided_instance:
            item["category_display"] = label_map.get(item["category"], item["category"])

        mooc_course_instance = list(mooc_course_instance.filter(email=faculty_instance).values('category', 'noc', 'begi_date','id'))
        for item in mooc_course_instance:
            item["category_display"] = label_map.get(item["category"], item["category"])

        patents_instance = list(patents_instance.filter(email=faculty_instance).values('id','gc','pd','top'))

        research_book_instance = list(research_book_instance.filter(email=faculty_instance).values('id','noa','pd','tob'))

        research_conference_instance = list(research_conference_instance.filter(email=faculty_instance).values('id','noa','pd','top'))

        research_journal_instance = list(research_journal_instance.filter(email=faculty_instance).values('id','noa','pd','noj'))

        resource_instance = list(resource_instance.filter(email=faculty_instance).values('category','toe','begi_date','id'))
        for item in resource_instance:
            item["category_display"] = label_map.get(item["category"], item["category"])

        sponsored_research_instance = list(sponsored_research_instance.filter(email=faculty_instance).values('category','nofa','created_at','id'))
        for item in sponsored_research_instance:
            item["category_display"] = label_map.get(item["category"], item["category"])

        context = {'form_type': form_type ,'nts': non_teaching_staff_instance ,'faa1': no_of_awards, 'eod1': events_instance,
                   'fdp1': faculty_participation_data, 'mp1': guided_instance, 'msc1': mooc_course_instance,
                   'patents1': patents_instance, 'rpb1': research_book_instance,
                   'rpcp1': research_conference_instance, 'rpj1': research_journal_instance,
                   'rp1': resource_instance, 'sgc1': sponsored_research_instance}

        return render(request, 'form_listing.html', context)

    elif pk == "partially_filled_forms" or pk == "more_explore_forms":

        return render(request, 'page_under_construction.html')
    else:
        return render(request,'404.html')
    
@session_login_required
def report(request):
    if request.session.get('topLeftBar') == 'spa' or request.session.get('topLeftBar') == 'ad':
        faculty_member = Faculty.objects.get(pk=request.session.get('user_id'))

        label_map = {choice.value: choice.label for choice in cat}
        department_map = {choice.value: choice.label for choice in department}
        index_by_map = {choice.value: choice.label for choice in index_by}
        level_map = {choice.value: choice.label for choice in level}
        top_map = {choice.value: choice.label for choice in type_of_patent}

        faculty_instance = list(Faculty.objects.filter(status="R").values('department').annotate(count=Count('id')))
        for item in faculty_instance:
            item['category'] = item['department']
            item['category_display'] = department_map.get(item['category'], item['category'])

        non_teaching_instance = non_teaching_staff.objects.all().count()

        no_of_awards = list(
            awards_and_achievments.objects.all().values('category').annotate(count=Count('id')))
        for item in no_of_awards:
            item['category_display'] = label_map.get(item['category'], item['category'])

        events_instance = list(events.objects.all().values('category').annotate(count=Count('id')))
        for item in events_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        faculty_participartion_data = list(
            Faculty_participation_data.objects.all().values('category').annotate(
                count=Count('id')))
        for item in faculty_participartion_data:
            item['category_display'] = label_map.get(item['category'], item['category'])

        guided_instance = list(guided.objects.all().values('category').annotate(count=Count('id')))
        for item in guided_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        mooc_course_instance = list(
            mooc_course.objects.all().values('category').annotate(count=Count('id')))
        for item in mooc_course_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        patents_instance = list(patents.objects.all().values('pg').annotate(count=Count('id')))
        for item in patents_instance:
            item['category'] = item['pg']
            item['category_display'] = top_map.get(item['category'], item['category'])

        research_book_instance = list(research_book.objects.all().values('level').annotate(count=Count('id')))
        for item in research_book_instance:
            item['category'] = item['level']
            item['category_display'] = level_map.get(item['category'], item['category'])

        research_conference_instance = list(research_conference.objects.all().values('level').annotate(count=Count('id')))
        for item in research_conference_instance:
            item['category'] = item['level']
            item['category_display'] = level_map.get(item['category'], item['category'])

        research_journal_instance = list(research_journal.objects.all().values('index_by').annotate(count=Count('id')))
        for item in research_journal_instance:
            item['category'] = item['index_by']
            item['category_display'] = index_by_map.get(item['category'], item['category'])

        resource_instance = list(
            resource.objects.all().values('category').annotate(count=Count('id')))
        for item in resource_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        sponsored_research_instance = list(
            sponsored_research.objects.all().values('category').annotate(count=Count('id')))
        for item in sponsored_research_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        paired_form = zip(faculty_member.form_alloted, faculty_member.form_alloted_display_list)

        context = {'user': request.session.get('topLeftBar'), 'fac_ins': Faculty.objects.filter(status="R"),
                   'non_teaching': non_teaching_staff.objects.all(), 'faa1': awards_and_achievments.objects.all(),
                   'eod1': events.objects.all(),
                   'fdp1': Faculty_participation_data.objects.all(), 'mp1': guided.objects.all(),
                   'msc1': mooc_course.objects.all(),
                   'patents1': patents.objects.all(), 'rpb1': research_book.objects.all(),
                   'rpcp1': research_conference.objects.all(),
                   'rpj1': research_journal.objects.all(), 'rp1': resource.objects.all(),
                   'sgc1': sponsored_research.objects.all(),'form_to_show' : list(paired_form),
                   'f_no' : faculty_member.form_alloted, 'f_1_1': faculty_instance, 'f_1_2': non_teaching_instance,
                   'f_2': faculty_participartion_data, 'f_3' : mooc_course_instance, 'f_4': events_instance,
                   'f_5': no_of_awards, 'f_6': sponsored_research_instance,'f_7_1': research_journal_instance,
                   'f_7_2': research_conference_instance, 'f_7_3': research_book_instance, 'f_7_4': patents_instance,
                   'f_8': guided_instance, 'f_9': resource_instance}

        return render(request, 'entire_report.html', context)
    else:
        return render(request, '404.html')