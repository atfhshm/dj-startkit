from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from apps.api.v1.user.serializers import UserSerializer
from apps.organization.models import Invitation, Member, Organization

__all__ = [
    "MinimalOrganizationSerializer",
    "OrganizationSerializer",
    "MinimalMemberSerializer",
    "MemberSerializer",
    "CreateInvitationSerializer",
    "MinimalInvitationSerializer",
    "InvitationSerializer",
]


class MinimalOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "slug",
            "avatar",
            "owner",
            "status",
            "country",
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    country = CountryField(country_dict=True)

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "slug",
            "avatar",
            "status",
            "owner",
            "country",
            "created_at",
            "updated_at",
        ]


class MinimalMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "organization",
            "user",
            "role",
            "is_active",
        ]


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    organization = MinimalOrganizationSerializer()

    class Meta:
        model = Member
        fields = [
            "id",
            "organization",
            "user",
            "role",
            "is_active",
        ]


class CreateInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = (
            "email",
            "role",
        )


class MinimalInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = [
            "id",
            "email",
            "role",
            "invited_by",
            "status",
            "expired_at",
        ]
        read_only_fields = ("token",)


class InvitationSerializer(serializers.ModelSerializer):
    invited_by = UserSerializer()
    organization = MinimalOrganizationSerializer()

    class Meta:
        model = Invitation
        fields = [
            "id",
            "email",
            "role",
            "invited_by",
            "organization",
            "status",
            "expired_at",
        ]
