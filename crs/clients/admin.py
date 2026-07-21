from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'telegram', 'organization', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'phone')

