from django.urls import path
from firstWebsite import views

urlpatterns = [
    path('', views.index, name = "home"),
    path('profile', views.profile, name = "profile"),
    path('allocated_batches', views.allocated_batches, name = "allocated-batches"),
    path('student_directory', views.student_directory, name = "student-directory"),
    path('about', views.about, name = "about"),
    path('batch/<str:pk>', views.stu_card_details, name = "batch"),
    path('login', views.login_page, name = "login"),
    path('auth/google/gsi-verify/', views.gsi_verify_login, name='gsi_verify_login'),
    path('logout', views.custom_logout, name='logout'),
    path('upload_excel', views.upload_excel, name='upload_excel'),
    path('fdp', views.fdp, name='fdp'),
    path('all_forms/<int:pk>', views.all_forms, name='all_forms'),
    path('save_all_forms/<int:pk>',views.save_all_forms, name="save_all_forms"),
    path('success',views.successfulsubmission, name="success"),
    path('progress',views.progress,name="progress"),
    path('edit_profile',views.edit_profile,name="editProfile")
]