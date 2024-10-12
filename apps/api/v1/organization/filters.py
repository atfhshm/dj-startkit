from django_filters import rest_framework as drf

from apps.organization.models import Invitation, Member, Organization

__all__ = [
    "OrganizationFilter",
    "MemberFilter",
    "InvitationFilter",
]


class OrganizationFilter(drf.FilterSet):
    created_at = drf.DateFromToRangeFilter()

    class Meta:
        model = Organization
        fields = (
            "name",
            "country",
            "status",
            "created_at",
        )


class MemberFilter(drf.FilterSet):
    class Meta:
        model = Member
        # TODO: add name filter
        fields = (
            "role",
            "is_active",
        )


class InvitationFilter(drf.FilterSet):
    class Meta:
        model = Invitation
        fields = (
            "status",
            "email",
        )
