import jwt
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse

from MyFirstDjangoWebsite import settings
from firstWebsite.modals import non_teaching_staff, Faculty_participation_data, mooc_course, events, \
    awards_and_achievments, sponsored_research, research_journal, research_conference, research_book, patents, guided, \
    resource

# Try to send redirect back to progressDetails/filled_forms for forms 0, 1, 2 etc.
def deleteformdata(request):
    if request.method == "POST":
        form_no = request.POST.get('form_no')
        user_token = request.POST.get('pk')
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        actual_pk = payload['user_pk']
        if form_no == "1_2":
            non_teaching_staff_instance = get_object_or_404(non_teaching_staff, pk=actual_pk)
            non_teaching_staff_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "2":
            faculty_participation_data_instance = get_object_or_404(Faculty_participation_data, pk=actual_pk)
            faculty_participation_data_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "3":
            moon_course_instance = get_object_or_404(mooc_course, pk=actual_pk)
            moon_course_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "4":
            events_instance = get_object_or_404(events, pk=actual_pk)
            events_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "5":
            awards_instance = get_object_or_404(awards_and_achievments, pk=actual_pk)
            awards_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "6":
            sponsored_research_instance = get_object_or_404(sponsored_research, pk=actual_pk)
            sponsored_research_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "7_1":
            research_journal_instance = get_object_or_404(research_journal, pk=actual_pk)
            research_journal_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "7_2":
            research_conference_instance = get_object_or_404(research_conference, pk=actual_pk)
            research_conference_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "7_3":
            research_book_instance = get_object_or_404(research_book, pk=actual_pk)
            research_book_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "7_4":
            patents_instance = get_object_or_404(patents, pk=actual_pk)
            patents_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "8":
            guided_instance = get_object_or_404(guided, pk=actual_pk)
            guided_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "9":
            resource_instance = get_object_or_404(resource, pk=actual_pk)
            resource_instance.delete()
            messages.success(request,"Entry deleted successfully!")
        else:
            return render(request,'404.html')

    url = request.POST.get('next')
    tab_no = request.POST.get('tab_no')
    if tab_no is None:
        return redirect(url)
    else:
        return redirect(f"{url}?tab={tab_no}")
