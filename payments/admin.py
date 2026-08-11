from django.contrib import admin
from .models import BoostOrder


@admin.register(BoostOrder)
class BoostOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "boost_type", "amount_som", "status", "expires_at", "created_at")
    list_filter = ("boost_type", "status")
    search_fields = ("user__username", "payme_transaction_id")
    readonly_fields = [f.name for f in BoostOrder._meta.fields if f.name.startswith("payme_")]
