from django.urls import path
from firstWebsite import views, saveforms, uploadExcel, progress_track, download, deleteFormData

urlpatterns = [
    path('',views.index,name = "home"),
    path('dashboard', progress_track.progress_bar, name="progress"),
    path('profile', views.profile, name = "profile"),
    path('about', views.about, name = "about"),
    path('faculty/<str:department_val>', views.fac_card_details, name = "fac"),
    path('login', views.login_page, name = "login"),
    path('auth/google/gsi-verify/', views.gsi_verify_login, name='gsi_verify_login'),
    path('logout', views.custom_logout, name='logout'),
    path('upload_excel/<int:form_no>', uploadExcel.upload_excel, name='upload_excel'),
    path('fdp', views.fdp, name='fdp'),
    path('all_forms/<int:form_no>', views.all_forms, name='all_forms'),
    path('save_all_forms/<int:form_no>',saveforms.save_all_forms, name="save_all_forms"),
    path('edit_profile',views.edit_profile,name="editProfile"),
    path('manage_profile/<str:user_token>',views.edit_profile,name="manageProfile"),
    path('manage_access',views.manage_access,name="manage_access"),
    path('deleteUser',views.deleteuser,name="deleteUser"),
    path('download',download.download_files,name="download"),
    path('puc',views.page_under_construction,name="page_under_construction"),
    path('faq',views.faq,name="FaQ"),
    path('forms_listing/<str:form_type>',progress_track.forms_listing,name="form_listing"),
    path('report',progress_track.report,name="report"),
    path('cookie',views.cookie_not_found,name="cookie"),
    path('deleteformdata',deleteFormData.deleteformdata,name="deleteEntry"),
    path('forms_listing/progressdetails/<str:form_no>/<str:user_token>',views.progressdetails,name="progressDetails"), # Security Breach Possible
    path('edit_form/<str:form_no>/<str:user_token>',saveforms.editforms,name="editForms"), # Security Breach Possible
    path('faculty/<str:user_token>/detailed-info-profile/',views.detailed_info_profile,name="detailed-info-profile"), # Security Breach Possible
    path('forms_report',progress_track.showdynamictable, name="formsReport")
]