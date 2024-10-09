from django.contrib.auth import authenticate, login
from drf_spectacular.utils import OpenApiExample, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.api.v1.auth.schema import INVALID_USER_REGISTER_SCHEMA
from apps.user.models import User

from .serializers import (
    TokenObtainPairResponseSerializer,
    TokenObtainPairSerializer,
    TokenRefreshResponseSerializer,
    UserRegisterSerializer,
)

__all__ = []


@extend_schema(
    description="Takes a set of user credentials and returns a user object with an access and refresh JSON web token pair.",
    tags=["auth"],
    request=TokenObtainPairSerializer,
    responses={
        status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name="InvalidCredentials",
            fields={"detail": serializers.CharField(max_length=128)},
        ),
    },
    examples=[
        OpenApiExample(
            "InvalidCredentials",
            value={"detail": "Invalid credentials."},
            status_codes=[status.HTTP_401_UNAUTHORIZED],
            response_only=True,
        )
    ],
)
class TokenPairObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        login_term: str = request.data.get("login")
        password: str = request.data.get("password")
        # TODO: implement an authentication backend that user email, username or phone number
        user: User | None = authenticate(request, email=login_term, password=password)
        if user:
            login(request, user)
            serializer = TokenObtainPairResponseSerializer(instance=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@extend_schema(
    tags=["auth"],
    responses={
        status.HTTP_200_OK: TokenRefreshResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name="InvalidAccessToken",
            fields={
                "detail": serializers.CharField(max_length=30),
                "code": serializers.CharField(max_length=30),
            },
        ),
    },
    examples=[
        OpenApiExample(
            response_only=True,
            name="InvalidAccessToken",
            status_codes=[status.HTTP_401_UNAUTHORIZED],
            value={
                "detail": "Token is invalid or expired",
                "code": "token_not_valid",
            },
        ),
    ],
)
class TokenRefreshObtainView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class VerifyTokenView(TokenVerifyView):
    @extend_schema(
        tags=["auth"],
        responses={
            status.HTTP_200_OK: {},
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name="InvalidToken",
                fields={
                    "detail": serializers.CharField(),
                    "code": serializers.CharField(),
                },
            ),
        },
        examples=[
            OpenApiExample(
                name="InvalidToken",
                status_codes=[
                    status.HTTP_401_UNAUTHORIZED,
                ],
                response_only=True,
                value={
                    "detail": "Token is invalid or expired",
                    "code": "token_not_valid",
                },
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    description="Takes the user object and create a new user if the user object is valid else raise exceptions",
    tags=["auth"],
    request=UserRegisterSerializer,
    responses={
        status.HTTP_201_CREATED: TokenObtainPairResponseSerializer,
        status.HTTP_400_BAD_REQUEST: UserRegisterSerializer,
    },
    examples=[
        OpenApiExample(
            name="InvalidRegister",
            status_codes=[
                status.HTTP_400_BAD_REQUEST,
            ],
            value=INVALID_USER_REGISTER_SCHEMA,
            response_only=True,
        )
    ],
)
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token_pair_serializer = TokenObtainPairResponseSerializer(instance=user)
            return Response(
                data=token_pair_serializer.data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: Implement magic link authentication
