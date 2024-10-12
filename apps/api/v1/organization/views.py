from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.organization.filters import (
    InvitationFilter,
    MemberFilter,
    OrganizationFilter,
)
from apps.api.v1.organization.serializers import (
    CreateInvitationSerializer,
    InvitationSerializer,
    MemberSerializer,
    MinimalInvitationSerializer,
    MinimalMemberSerializer,
    MinimalOrganizationSerializer,
    OrganizationSerializer,
)
from apps.organization.models import Invitation, Member, Organization
from core.pagination import PagePaginator

__all__ = [
    "ListCreateOrganizationView",
    "RetrieveUpdateDestroyOrganizationView",
    "ListMemberView",
    "RetrieveUpdateDestroyMemberView",
    "ListInvitationView",
    "InviteMemberView",
    "AcceptInvitationView",
]


@extend_schema(
    summary="List and create organizations",
    description="List and create organizations",
    tags=["organizations"],
)
class ListCreateOrganizationView(ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PagePaginator
    filterset_class = OrganizationFilter

    def get_queryset(self):
        qs = Organization.objects.select_related(
            "owner",
        )
        return qs


class RetrieveUpdateDestroyOrganizationView(RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = MinimalOrganizationSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    http_method_names = ["get", "patch", "delete"]

    @extend_schema(
        summary="Get an organization",
        description="Get an organization",
        tags=["organizations"],
        responses={
            status.HTTP_200_OK: MinimalOrganizationSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update an organization",
        description="Update an organization",
        tags=["organizations"],
        request=MinimalOrganizationSerializer,
        responses={
            status.HTTP_200_OK: MinimalOrganizationSerializer,
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an organization",
        description="Delete an organization",
        tags=["organizations"],
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@extend_schema(
    summary="List organization members",
    description="List organization members",
    tags=["organization members"],
)
class ListMemberView(ListAPIView):
    queryset = Member.objects.select_related("organization").all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PagePaginator
    filterset_class = MemberFilter
    lookup_url_kwarg = "slug"
    lookup_field = "organization__slug"


@extend_schema(
    summary="Retrieve, update or delete an organization member",
    description="Retrieve, update or delete an organization member",
    tags=["organization members"],
)
class RetrieveUpdateDestroyMemberView(RetrieveUpdateDestroyAPIView):
    serializer_class = MinimalMemberSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "delete"]

    def get_object(self):
        organization_slug = self.kwargs["slug"]
        member_id = self.kwargs["id"]
        obj = get_object_or_404(
            Member, organization__slug=organization_slug, id=member_id
        )
        return obj


@extend_schema(
    summary="List organization invitations",
    description="List organization invitations",
    tags=["organization members"],
)
class ListInvitationView(ListAPIView):
    queryset = Invitation.objects.select_related(
        "organization",
        "invited_by",
    ).all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PagePaginator
    filterset_class = InvitationFilter
    lookup_url_kwarg = "slug"
    lookup_field = "organization__slug"


class InviteMemberView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MinimalInvitationSerializer

    @extend_schema(
        summary="Invite a new member to the organization",
        description="Invite a new member to the organization",
        tags=["organization invitations"],
        request=CreateInvitationSerializer,
        responses={201: MinimalInvitationSerializer},
    )
    def post(self, request: Request, slug: str) -> Response:
        invited_by = self.request.user
        organization = get_object_or_404(Organization, slug=slug)
        data = request.data.copy()
        data["organization"] = organization.id
        serializer = CreateInvitationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # TODO: send an invitation via email
        # TODO: email url, frontend, ?organization_slug=slug&token=token
        serializer.save(
            invited_by=invited_by,
            organization=organization,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# TODO: Add verify token

class AcceptInvitationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Accept an invitation to join the organization",
        description="Accept an invitation to join the organization",
        tags=["organization invitations"],
        request=None,
        responses={
            status.HTTP_200_OK: MemberSerializer,
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        token = self.kwargs["token"]
        invitation = get_object_or_404(Invitation, token=token)
        # TODO: insert a new member
        if invitation.valid:
            invitation.status = Invitation.InvitationStatus.ACCEPTED
            invitation.save()
            return Response(
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
