from django.contrib import admin, messages
from .models import Organization, Application


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "type", "tariff", "is_active", "created_at")
    list_filter = ("type", "tariff", "is_active", "currency")
    search_fields = ("name", "phone", "external_id")
    list_display_links = ('name', 'phone')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "type", "tariff", "status", "created_at")
    list_filter = ("status", "type", "tariff")
    search_fields = ("name", "phone")
    readonly_fields = ("organization", "processed_at", "created_at")
    actions = ["approve_applications", "reject_applications"]

    @admin.action(description="Одобрить заявку и создать организацию")
    def approve_applications(self, request, queryset):
        approved = 0
        errors = []
        for application in queryset:
            if application.status != "APPROVED":
                try:
                    application.approve()
                    approved += 1
                except ValueError as e:
                    errors.append(str(e))

        if approved:
            self.message_user(request, f"Одобрено заявок: {approved}. Организации созданы с is_active=False — включите после оплаты.")
        if errors:
            self.message_user(request, "Не удалось одобрить: " + " ".join(errors), level=messages.WARNING)

    @admin.action(description="Отклонить заявку")
    def reject_applications(self, request, queryset):
        rejected = queryset.exclude(status="APPROVED").update(status="REJECTED")
        self.message_user(request, f"Отклонено заявок: {rejected}")