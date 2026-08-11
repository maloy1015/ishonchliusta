from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.splash_view, name="splash"),
]
