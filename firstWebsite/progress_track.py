from django.shortcuts import render
from django.contrib import messages
from django.db.models import Count
from firstWebsite.modals import Faculty, awards_and_achievments, category as cat, events, Faculty_participation_data, \
    guided, mooc_course, patents, research_book, research_conference, research_journal, resource, sponsored_research
from firstWebsite.views import session_login_required


@session_login_required
def progress_bar(request):
    try:
        email = Faculty.objects.get(pk=request.session.get('user_id'))

        label_map = {choice.value: choice.label for choice in cat}

        no_of_awards = list(awards_and_achievments.objects.filter(email=email).values('category').annotate(count=Count('id')))
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
    except Faculty.DoesNotExist:
        error_message = f"User does not exist in database."
        messages.error(request,error_message)
        return render(request,'index.html')