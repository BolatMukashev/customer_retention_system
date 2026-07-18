from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('organization', 'client', 'person_name', 'relation', 'event_type', 'event_date')
    list_filter = ('organization', 'event_type', 'relation')
    search_fields = ('person_name',)
    ordering = ('event_date',)
