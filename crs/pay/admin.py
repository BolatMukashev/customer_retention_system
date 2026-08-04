from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("organization", "amount", "paid_at", "created_at")
    list_filter = ("paid_at",)
    search_fields = ("organization__name", "organization__phone")
    autocomplete_fields = ("organization",)
    ordering = ("-paid_at",)