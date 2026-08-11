from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path("royhat/", views.register_view, name="register"),
    path("kirish/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("chiqish/", auth_views.LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("kabinet/", views.dashboard_view, name="dashboard"),
    path("profil/tahrirlash/", views.profile_edit_view, name="profile_edit"),
    path("profil/ochirish/", views.delete_account_view, name="delete_account"),
    path("profil/<int:pk>/", views.profile_detail_view, name="profile_detail"),
    path("lokatsiya/belgilash/", views.location_picker_view, name="location_picker"),
    path("lokatsiya/yangilash/", views.update_location_view, name="update_location"),
]
