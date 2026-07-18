from django.contrib import admin
from .models import Referral

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'phone', 'is_active')
    search_fields = ('referrer__first_name', 'referred__first_name')
    list_filter = ('first_name', 'phone', 'is_active')
    ordering = ('first_name', 'phone', 'is_active')
