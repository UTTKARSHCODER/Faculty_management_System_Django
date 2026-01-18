from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from firstWebsite.modals import non_teaching_staff, Faculty_participation_data, mooc_course, events, \
    awards_and_achievments, sponsored_research, research_journal, research_conference, research_book, patents, guided, \
    resource


def deleteformdata(request, pk):
    if request.method == "POST":
        form_no = request.POST.get('form_no')
        if form_no == "16":
            entry_pk = request.POST.get('pk')
            non_teaching_staff_instance = get_object_or_404(non_teaching_staff, pk=entry_pk)
            non_teaching_staff_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "1":
            entry_pk = request.POST.get('pk')
            faculty_participation_data_instance = get_object_or_404(Faculty_participation_data, pk=entry_pk)
            faculty_participation_data_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "2":
            entry_pk = request.POST.get('pk')
            moon_course_instance = get_object_or_404(mooc_course, pk=entry_pk)
            moon_course_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "3":
            entry_pk = request.POST.get('pk')
            events_instance = get_object_or_404(events, pk=entry_pk)
            events_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "4":
            entry_pk = request.POST.get('pk')
            awards_instance = get_object_or_404(awards_and_achievments, pk=entry_pk)
            awards_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "5":
            entry_pk = request.POST.get('pk')
            sponsored_research_instance = get_object_or_404(sponsored_research, pk=entry_pk)
            sponsored_research_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "6":
            entry_pk = request.POST.get('pk')
            research_journal_instance = get_object_or_404(research_journal, pk=entry_pk)
            research_journal_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "7":
            entry_pk = request.POST.get('pk')
            research_conference_instance = get_object_or_404(research_conference, pk=entry_pk)
            research_conference_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "8":
            entry_pk = request.POST.get('pk')
            research_book_instance = get_object_or_404(research_book, pk=entry_pk)
            research_book_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "9":
            entry_pk = request.POST.get('pk')
            patents_instance = get_object_or_404(patents, pk=entry_pk)
            patents_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "10":
            entry_pk = request.POST.get('pk')
            guided_instance = get_object_or_404(guided, pk=entry_pk)
            guided_instance.delete()
            messages.success(request,"Entry deleted successfully!")

        elif form_no == "11":
            entry_pk = request.POST.get('pk')
            resource_instance = get_object_or_404(resource, pk=entry_pk)
            resource_instance.delete()
            messages.success(request,"Entry deleted successfully!")
        else:
            return render(request,'404.html')
    return redirect('form_listing',pk=pk)