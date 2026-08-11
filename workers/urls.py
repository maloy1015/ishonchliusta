from django.urls import path
from . import views

app_name = "workers"

urlpatterns = [
    path("ustalar/", views.worker_list_view, name="worker_list"),
    path("post/qoshish/", views.post_create_view, name="post_create"),
    path("post/<int:pk>/ochirish/", views.post_delete_view, name="post_delete"),
]
