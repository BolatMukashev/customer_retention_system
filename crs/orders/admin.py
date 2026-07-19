from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'client', 'amount', 'created_at')
    list_filter = ('organization', 'client', 'created_at')
    search_fields = ('organization__name', 'client__name', 'client__phone')

