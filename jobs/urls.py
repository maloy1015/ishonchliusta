from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("ishlar/", views.job_list_view, name="job_list"),
    path("ishlar/elon-berish/", views.job_create_view, name="job_create"),
    path("ishlar/mening-elonlarim/", views.my_jobs_view, name="my_jobs"),
    path("ishlar/<int:pk>/holat/", views.job_toggle_status_view, name="job_toggle_status"),
    path("ishlar/<int:pk>/ochirish/", views.job_delete_view, name="job_delete"),
]
