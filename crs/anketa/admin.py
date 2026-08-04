from django.contrib import admin
from .models import RewardStep

@admin.register(RewardStep)
class RewardStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'position', 'title')
    list_filter = ('organization',)
    search_fields = ('title',)