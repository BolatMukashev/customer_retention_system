from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'tariff', 'is_active', 'created_at', 'last_payment_date')
    list_filter = ('tariff', 'is_active')
    search_fields = ('name', 'phone')
    ordering = ('name',)
