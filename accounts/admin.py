from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "first_name", "role", "phone", "category", "is_staff", "created_at")
    list_filter = ("role", "is_staff", "category")
    search_fields = ("username", "first_name", "phone")
    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumotlar", {"fields": (
            "role", "phone", "bio", "profile_image", "category", "experience_years",
            "latitude", "longitude"
        )}),
    )
