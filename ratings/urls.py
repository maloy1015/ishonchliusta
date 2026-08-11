from django.urls import path
from . import views

app_name = "ratings"

urlpatterns = [
    path("baholash/<int:pk>/", views.rate_worker_view, name="rate_worker"),
    path("reyting/", views.leaderboard_view, name="leaderboard"),
]
