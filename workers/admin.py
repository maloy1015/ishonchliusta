from django.contrib import admin
from .models import WorkerCategory, Post


@admin.register(WorkerCategory)
class WorkerCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "order")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("worker", "caption", "created_at")
    list_filter = ("worker",)
