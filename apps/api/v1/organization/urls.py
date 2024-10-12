from django.urls import path

from apps.api.v1.organization.views import (
    AcceptInvitationView,
    InviteMemberView,
    ListCreateOrganizationView,
    ListInvitationView,
    ListMemberView,
    RetrieveUpdateDestroyMemberView,
    RetrieveUpdateDestroyOrganizationView,
)

urlpatterns = [
    path(
        "<str:slug>",
        RetrieveUpdateDestroyOrganizationView.as_view(),
        name="get-update-destroy-organization",
    ),
    path(
        "",
        ListCreateOrganizationView.as_view(),
        name="list-create-organization",
    ),
    path(
        "<str:slug>/members",
        ListMemberView.as_view(),
        name="list-members",
    ),
    path(
        "<str:slug>/members/<str:id>",
        RetrieveUpdateDestroyMemberView.as_view(),
        name="list-members",
    ),
    path(
        "<str:slug>/invitations",
        ListInvitationView.as_view(),
        name="list-invitations",
    ),
    path(
        "<str:slug>/invitations/invite",
        InviteMemberView.as_view(),
        name="invite-member",
    ),
    path(
        "<str:slug>/invitations/<str:token>/accept",
        AcceptInvitationView.as_view(),
        name="accept-invitation",
    ),
]
