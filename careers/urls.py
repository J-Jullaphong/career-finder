from django.urls import path
from .views import homepage, custom_login, custom_logout, job_search, \
    JobSeekerRegistrationView, \
    CompanyRegistrationView, recruiter_registration_view, JobSeekerProfileView, \
    CompanyProfileView, RecruiterProfileView, \
    manage_job_openings, apply, MyApplicationView, \
    CompanyRecruiterManagementView, \
    post_job_opening, update_job_description, delete_application, \
    delete_job_opening, view_job_seeker, update_recruiter, delete_recruiter, \
    RecruiterJobApplicationView

app_name = 'careers'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('register/job_seeker/', JobSeekerRegistrationView.as_view(),
         name='job_seeker_register'),
    path('register/company/', CompanyRegistrationView.as_view(),
         name='company_register'),
    path('job_search/', job_search, name='job_search'),
    path('job_seeker/<str:job_seeker_id>/', JobSeekerProfileView.as_view(),
         name='job_seeker_profile'),
    path('company/<str:company_id>/', CompanyProfileView.as_view(),
         name='company_profile'),
    path('recruiter/<str:recruiter_id>/', RecruiterProfileView.as_view(),
         name='recruiter_profile'),
    path('company/<str:company_id>/recruiters/register/',
         recruiter_registration_view, name='recruiter_register'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('company/<str:company_id>/jobs/', manage_job_openings,
         name='manage_job_openings'),
    path('company/<str:company_id>/recruiters/',
         CompanyRecruiterManagementView.as_view(),
         name='recruiter_management'),
    path('apply/<str:job_opening_id>/', apply, name='apply'),
    path('my_applications/', MyApplicationView.as_view(),
         name='my_applications'),
    path('recruiter_job_applications/', RecruiterJobApplicationView.as_view(),
         name='recruiter_job_applications'),
    path('company/<str:company_id>/post_job/', post_job_opening,
         name='post_job_opening'),
    path('company/<str:company_id>/update_job/<str:job_opening_id>/',
         update_job_description, name='update_job_description'),
    path('delete_application/<str:job_opening_id>/', delete_application,
         name='delete_application'),
    path('company/<str:company_id>/delete_job/<str:job_opening_id>/',
         delete_job_opening, name='delete_job_opening'),
    path('company/<str:company_id>/update_recruiter/<str:recruiter_id>/',
         update_recruiter, name='update_recruiter'),
    path('company/<str:company_id>/delete_recruiter/<str:recruiter_id>/',
         delete_recruiter, name='delete_recruiter'),
    path('view_job_seekers/', view_job_seeker, name='view_job_seekers'),
]
