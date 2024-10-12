from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.user.filters import UserFilter
from apps.api.v1.user.schema import (
    UserNotFoundExample,
    InvalidUpdateUserExample,
    InvalidPasswordExample,
)
from apps.api.v1.user.serializers import (
    PasswordChangeSerializer,
    UserSerializer,
)
from apps.user.models import User
from core.pagination import PagePaginator
from core.serializers import NotFoundSerializer

__all__ = [
    "GetCurrentUserView",
    "RetrieveUpdateDestroyUserView",
    "UserListView",
    "PasswordChangeView",
]


@extend_schema(
    summary="Get authenticated user",
    description="Get the current authenticated user data",
    tags=["users"],
    responses={
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
    },
    examples=[
        UserNotFoundExample,
    ],
)
class GetCurrentUserView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RetrieveUpdateDestroyUserView(RetrieveUpdateDestroyAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "delete"]

    @extend_schema(
        summary="Retrieve user by email",
        description="Retrieve user by email",
        tags=["users"],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        examples=[
            UserNotFoundExample,
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update user by email",
        description="Update user by email",
        tags=["users"],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: UserSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        examples=[
            UserNotFoundExample,
            InvalidUpdateUserExample,
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete user by email",
        description="Delete user by email",
        tags=["users"],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        examples=[
            UserNotFoundExample,
        ],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@extend_schema(
    summary="List users",
    description="A paginated and filtered list of users",
    tags=["users"],
)
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PagePaginator
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter


@extend_schema(
    summary="Change user password",
    description="Takes the old password, new password and confirm new password to change the user password.",
    tags=["users"],
    request=PasswordChangeSerializer,
    responses={
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: PasswordChangeSerializer,
    },
    examples=[InvalidPasswordExample],
)
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.request.user.pk)
        password = self.request.data.get("password")
        new_password = self.request.data.get("new_password")
        if not user.check_password(password):
            return Response(
                data={"password": ["Invalid password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)
