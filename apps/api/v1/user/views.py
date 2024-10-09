from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiExample, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.user.filters import UserFilter
from apps.api.v1.user.schema import (
    InvalidPassword,
    InvalidUserUpdate,
    UserNotFoundExample,
    UserNotFoundSchema,
)
from apps.api.v1.user.serializers import PasswordChangeSerializer, UserSerializer
from apps.user.models import User
from core.pagination import PagePaginator


class RetrieveUpdateDestroyUserView(RetrieveUpdateDestroyAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "patch", "delete"]

    @extend_schema(
        description="Retrieve a user instance",
        tags=["users"],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_404_NOT_FOUND: UserNotFoundSchema,
        },
        examples=[
            OpenApiExample(
                name="UserNotFound",
                response_only=True,
                status_codes=[status.HTTP_404_NOT_FOUND],
                value=UserNotFoundExample,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Update a user instance",
        tags=["users"],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_404_NOT_FOUND: UserNotFoundSchema(),
        },
        examples=[
            OpenApiExample(
                name="UserNotFound",
                response_only=True,
                status_codes=[status.HTTP_404_NOT_FOUND],
                value=UserNotFoundExample,
            ),
            OpenApiExample(
                name="InvalidUserUpdate",
                response_only=True,
                status_codes=[status.HTTP_400_BAD_REQUEST],
                value=InvalidUserUpdate,
            ),
        ],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        description="Delete a user instance",
        tags=["users"],
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: UserNotFoundSchema,
        },
        examples=[
            OpenApiExample(
                name="UserNotFound",
                response_only=True,
                status_codes=[status.HTTP_404_NOT_FOUND],
                value=UserNotFoundExample,
            )
        ],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@extend_schema(
    description="list users view",
    tags=["users"],
)
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PagePaginator
    permission_classes = [IsAuthenticated]
    filterset_class = UserFilter
    ordering_fields = ["id", "date_joined"]
    ordering = ["id"]


@extend_schema(
    description="Takes the old password, new password and confirm new password to change the user password.",
    tags=["users"],
    request=PasswordChangeSerializer,
    responses={
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name="InvalidPassword",
            fields={
                "password": serializers.CharField(max_length=132),
                "new_password": serializers.CharField(max_length=132),
            },
        ),
    },
    examples=[
        OpenApiExample(
            name="InvalidPassword",
            response_only=True,
            status_codes=[status.HTTP_400_BAD_REQUEST],
            value=InvalidPassword,
        ),
    ],
)
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=self.request.user.pk)
        password = self.request.data.get("password")
        new_password = self.request.data.get("new_password")
        if not user.check_password(password):
            return Response(
                data={"password": ["Invalid password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
