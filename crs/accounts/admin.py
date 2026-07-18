from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("id",)

    list_display = (
        "id",
        "phone",
        "first_name",
        "last_name",
        "organization",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "phone",
        "first_name",
        "last_name",
    )

    fieldsets = (
        (None, {
            "fields": (
                "phone",
                "password",
            )
        }),
        ("Личная информация", {
            "fields": (
                "first_name",
                "last_name",
                "organization",
            )
        }),
        ("Права доступа", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Даты", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone",
                "password1",
                "password2",
                "organization",
                "is_active",
                "is_staff",
                "is_superuser",
            ),
        }),
    )