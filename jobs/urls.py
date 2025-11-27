from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    
    path("", views.job_list, name="list"),
    path("<int:pk>/", views.job_detail, name="detail"),

   
    path("employer/mine/", views.employer_jobs, name="employer_jobs"),
    path("employer/create/", views.job_create, name="create"),
    path("employer/<int:pk>/edit/", views.job_edit, name="edit"),


    path("<int:pk>/apply/", views.apply_to_job, name="apply"),  # pk = job id
    path("applications/mine/", views.my_applications, name="my_applications"),
    path("employer/<int:pk>/applicants/", views.job_applicants, name="job_applicants"),  # pk = job id
    path("applications/<int:app_id>/resume/", views.download_resume, name="download_resume"),
    path("applications/<int:app_id>/status/", views.update_application_status, name="update_application_status"),
]