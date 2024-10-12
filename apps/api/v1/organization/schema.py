from drf_spectacular.utils import OpenApiExample
from rest_framework import status

OrganizationNotFoundExample = OpenApiExample(
    name="OrganizationNotFound",
    value={},
    status_codes=[status.HTTP_404_NOT_FOUND],
    response_only=True,
)
MemberNotFoundExample = OpenApiExample(
    name="MemberNotFound",
    value={},
    status_codes=[status.HTTP_404_NOT_FOUND],
    response_only=True,
)
InvitationNotFoundExample = OpenApiExample(
    name="InvitationNotFound",
    value={},
    status_codes=[status.HTTP_404_NOT_FOUND],
    response_only=True,
)
