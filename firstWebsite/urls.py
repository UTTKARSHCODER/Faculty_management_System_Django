from django.urls import path
from firstWebsite import views, saveforms, uploadExcel, progress_track, download

urlpatterns = [
    path('', views.index, name = "home"),
    path('student', views.student, name = "student"),
    path('faculty', views.faculty, name = "faculty"),
    path('profile', views.profile, name = "profile"),
    path('student_directory', views.student_directory, name = "student-directory"),
    path('about', views.about, name = "about"),
    path('student/<str:pk>', views.stu_card_details, name = "batch"),
    path('faculty/<str:pk>', views.fac_card_details, name = "fac"),
    path('login', views.login_page, name = "login"),
    path('auth/google/gsi-verify/', views.gsi_verify_login, name='gsi_verify_login'),
    path('logout', views.custom_logout, name='logout'),
    path('upload_excel/<int:pk>', uploadExcel.upload_excel, name='upload_excel'),
    path('fdp', views.fdp, name='fdp'),
    path('all_forms/<int:pk>', views.all_forms, name='all_forms'),
    path('save_all_forms/<int:pk>',saveforms.save_all_forms, name="save_all_forms"),
    path('success',views.successfulsubmission, name="success"),
    path('progress',progress_track.progress_bar,name="progress"),
    path('edit_profile',views.edit_profile,name="editProfile"),
    path('directory',views.directory,name="directory"),
    path('deleteUser',views.deleteuser,name="deleteUser"),
    path('faculty_report',views.faculty_report,name="faculty_report"),
    path('download',download.download_files,name="download"),
    path('puc',views.page_under_construction,name="page_under_construction"),
    path('faq',views.faq,name="FaQ"),
]