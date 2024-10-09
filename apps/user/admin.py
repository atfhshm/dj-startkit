from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from apps.user.models import User

admin.site.register(Permission)


@admin.register(User)
class UserAdminConfig(UserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "phone_number",
        "date_joined",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
    )
    readonly_fields = ["date_joined", "updated_at", "last_login"]

    fieldsets = (
        (
            "basic info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "phone_number",
                    "avatar",
                    "password",
                )
            },
        ),
        (
            "groups and permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "user status",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "important dates",
            {
                "fields": (
                    "date_joined",
                    "updated_at",
                    "last_login",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "phone_number",
                    "password1",
                    "password2",
                    "avatar",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("username", "email", "phone_number")
    filter_horizontal = []
    ordering = ("-id", "email")
