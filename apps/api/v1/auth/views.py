from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import OpenApiExample, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.api.v1.auth.schema import INVALID_USER_REGISTER_SCHEMA
from apps.user.models import User

from .serializers import (
    RequestPasswordResetSerializer,
    ResetPasswordSerializer,
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


class RequestPasswordResetView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # TODO: Use celery task
            send_mail(
                "Password Reset Request",
                f"Use this link to reset your password: {settings.FRONTEND_URL}/auth/reset-password/{uid}/{token}/",
                "from@example.com",
                [user.email],
                fail_silently=False,
            )

            return Response(
                data={
                    "detail": "A reset link has been sent to your email, please check it."
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={
                    "detail": "A reset link has been sent to your email, please check it."
                },
                status=status.HTTP_200_OK,
            )


class ResetPasswordView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=user_id)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data["password"])
        user.save()

        return Response(
            {"detail": "Password has been reset."}, status=status.HTTP_200_OK
        )
