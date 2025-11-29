from django.contrib import admin

from firstWebsite.modals import Contact, Student_Directory, Faculty, Faculty_participation_data, mooc_course, events, \
    awards_and_achievments, sponsored_research, research_journal, research_conference, research_book, patents, guided, \
    resource, non_teaching_staff

# Tester 3121
# Register your models here.
admin.site.register(Contact)
admin.site.register(Student_Directory)
admin.site.register(Faculty)
admin.site.register(Faculty_participation_data)
admin.site.register(mooc_course)
admin.site.register(events)
admin.site.register(awards_and_achievments)
admin.site.register(sponsored_research)
admin.site.register(research_journal)
admin.site.register(research_conference)
admin.site.register(research_book)
admin.site.register(patents)
admin.site.register(guided)
admin.site.register(resource)
admin.site.register(non_teaching_staff)