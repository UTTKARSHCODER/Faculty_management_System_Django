from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from firstWebsite.modals import Faculty, awards_and_achievments, category as cat, events, Faculty_participation_data, \
    guided, mooc_course, patents, research_book, research_conference, research_journal, resource, sponsored_research, \
    non_teaching_staff
from firstWebsite.views import session_login_required


@session_login_required
def progress_bar(request):
    try:
        faculty_instance = Faculty.objects.get(pk=request.session.get('user_id'))

        label_map = {choice.value: choice.label for choice in cat}

        no_of_awards = list(awards_and_achievments.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in no_of_awards:
            item['category_display'] = label_map.get(item['category'], item['category'])

        events_instance = list(events.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in events_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        faculty_participartion_data = list(Faculty_participation_data.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in faculty_participartion_data:
            item['category_display'] = label_map.get(item['category'], item['category'])

        guided_instance = guided.objects.filter(email=faculty_instance).count()

        mooc_course_instance = list(mooc_course.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in mooc_course_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        patents_instance = patents.objects.filter(email=faculty_instance).count()

        research_book_instance = research_book.objects.filter(email=faculty_instance).count()

        research_conference_instance = research_conference.objects.filter(email=faculty_instance).count()

        research_journal_instance = research_journal.objects.filter(email=faculty_instance).count()
        resource_instance = resource.objects.filter(email=faculty_instance).count()

        sponsored_research_instance = list(sponsored_research.objects.filter(email=faculty_instance).values('category').annotate(count=Count('id')))
        for item in sponsored_research_instance:
            item['category_display'] = label_map.get(item['category'], item['category'])

        total_forms = sum(item['count'] for item in no_of_awards) + sum(item['count'] for item in events_instance) + sum(item['count'] for item in faculty_participartion_data) + guided_instance + sum(item['count'] for item in mooc_course_instance) + patents_instance + research_book_instance + research_conference_instance + research_journal_instance + resource_instance + sum(item['count'] for item in sponsored_research_instance)

        total_remaining_field_forms = 33 - (len(no_of_awards) + len(events_instance) + len(faculty_participartion_data) + (1 if guided_instance > 0 else 0) + len(mooc_course_instance) + (1 if patents_instance > 0 else 0) + (1 if research_book_instance > 0 else 0) + (1 if research_conference_instance > 0 else 0) + (1 if research_journal_instance > 0 else 0) + (1 if resource_instance > 0 else 0) + len(sponsored_research_instance))

        context = {'total_forms': total_forms,'total_rff' : total_remaining_field_forms, 'faa1': no_of_awards, 'eod1': events_instance, 'fdp1': faculty_participartion_data, 'mp1': guided_instance, 'msc1' : mooc_course_instance, 'patents1': patents_instance, 'rpb1': research_book_instance, 'rpcp1': research_conference_instance, 'rpj1': research_journal_instance, 'rp1': resource_instance, 'sgc1': sponsored_research_instance}
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

        no_of_awards = no_of_awards.filter(email=faculty_instance).order_by('category')
        for item in no_of_awards:
            item.category_display = label_map.get(item.category, item.category)

        events_instance = events_instance.filter(email=faculty_instance).order_by('category')
        for item in events_instance:
            item.category_display = label_map.get(item.category, item.category)

        faculty_participation_data = faculty_participation_data.filter(email=faculty_instance).order_by('category')
        for item in faculty_participation_data:
            item.category_display = label_map.get(item.category, item.category)

        mooc_course_instance = mooc_course_instance.filter(email=faculty_instance).order_by('category')
        for item in mooc_course_instance:
            item.category_display = label_map.get(item.category, item.category)

        sponsored_research_instance = sponsored_research_instance.filter(email=faculty_instance).order_by(
            'category')
        for item in sponsored_research_instance:
            item.category_display = label_map.get(item.category, item.category)

        context = {'form_type': form_type, 'faa1': no_of_awards, 'eod1': events_instance,
                   'fdp1': faculty_participation_data, 'mp1': guided_instance, 'msc1': mooc_course_instance,
                   'patents1': patents_instance, 'rpb1': research_book_instance,
                   'rpcp1': research_conference_instance, 'rpj1': research_journal_instance,
                   'rp1': resource_instance, 'sgc1': sponsored_research_instance}

        return render(request, 'form_listing.html', context)
    elif pk == "report":
        context = {'non_teaching': non_teaching_staff_instance.all(),'faa1': no_of_awards.all(), 'eod1': events_instance.all(),
                   'fdp1': faculty_participation_data.all(), 'mp1': guided_instance.all(),
                   'msc1': mooc_course_instance.all(),
                   'patents1': patents_instance.all(), 'rpb1': research_book_instance.all(),
                   'rpcp1': research_conference_instance.all(),
                   'rpj1': research_journal_instance.all(), 'rp1': resource_instance.all(),
                   'sgc1': sponsored_research_instance.all()}

        return render(request, 'form_listing_dir.html', context)

    elif pk == "partially_filled_forms" or pk == "more_explore_forms":

        return render(request, 'page_under_construction.html')
    else:
        return render(request,'404.html')