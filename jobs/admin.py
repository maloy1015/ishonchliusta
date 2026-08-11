from django.contrib import admin
from .models import JobPost


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ("title", "employer", "category", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "employer__username")
