from django.contrib import admin

from apps.organization.models import (
    Invitation,
    Member,
    Organization,
)


@admin.register(Organization)
class OrganizationAdminConfig(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "owner",
        "country",
        "status",
        "created_at",
    )
    list_filter = (
        "country",
        "status",
    )
    search_fields = (
        "name",
        "slug",
    )


@admin.register(Member)
class MemberAdminConfig(admin.ModelAdmin):
    list_display = (
        "id",
        "organization",
        "user",
        "role",
        "is_active",
    )
    list_filter = (
        "role",
        "is_active",
    )
    search_fields = (
        "org__name",
        "org__slug",
    )


@admin.register(Invitation)
class InvitationAdminConfig(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "role",
        "status",
        "expired_at",
    )
    list_filter = (
        "status",
        "role",
    )
    search_fields = ("email",)
