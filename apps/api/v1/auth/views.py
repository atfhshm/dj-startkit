from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.api.v1.auth.schema import (
    InvalidPasswordResetExample,
    InvalidRegisterExample,
    InvalidAuthenticationExample,
    InvalidTokenExample,
)
from apps.api.v1.user.schema import UserNotFoundExample
from apps.user.models import User
from core.jwt import get_tokens

from apps.api.v1.auth.serializers import (
    RequestPasswordResetSerializer,
    ResetPasswordSerializer,
    TokenObtainPairSerializer,
    TokenRefreshResponseSerializer,
    UserRegisterSerializer,
    TokenPairSerializer,
    InvalidCredentialsSerializer,
    InvalidTokenSerializer,
)

__all__ = [
    "TokenPairObtainView",
    "TokenRefreshObtainView",
    "VerifyTokenView",
    "RegisterUserView",
    "RequestPasswordResetView",
    "ResetPasswordView",
]

from core.serializers import NotFoundSerializer


@extend_schema(
    summary="Get JWT auth tokens",
    description="Takes a set of user credentials and returns access and refresh JSON web token pair.",
    tags=["auth"],
    request=TokenObtainPairSerializer,
    responses={
        status.HTTP_200_OK: TokenPairSerializer,
        status.HTTP_401_UNAUTHORIZED: InvalidCredentialsSerializer,
    },
    examples=[
        InvalidAuthenticationExample,
    ],
)
class TokenPairObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        login_term: str = serializer.data.get("login")
        password: str = serializer.data.get("password")
        # TODO: implement an authentication backend that user email, username or phone number
        user: User | None = authenticate(request, email=login_term, password=password)
        if user:
            login(request, user)
            tokens: dict[str, str] = get_tokens(user)
            tokens_serializer = TokenPairSerializer(instance=tokens)
            return Response(data=tokens_serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = InvalidCredentialsSerializer(
                instance={"detail": "Invalid credentials"}
            )
            return Response(
                data=serializer.data,
                status=status.HTTP_401_UNAUTHORIZED,
            )


@extend_schema(
    summary="Refresh a JWT auth token",
    description="Takes a refresh JWT token and obtain a new refreshed access JWT token",
    tags=["auth"],
    responses={
        status.HTTP_200_OK: TokenRefreshResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: InvalidTokenSerializer,
    },
    examples=[InvalidTokenExample],
)
class TokenRefreshObtainView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class VerifyTokenView(TokenVerifyView):
    @extend_schema(
        summary="Verify a JWT auth token",
        description="Verify a JWT auth token and",
        tags=["auth"],
        responses={
            status.HTTP_200_OK: {},
            status.HTTP_401_UNAUTHORIZED: InvalidTokenSerializer,
        },
        examples=[InvalidTokenExample],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    summary="Register a new user",
    description="Takes the user object and create a new user if the user object is valid else raise exceptions",
    tags=["auth"],
    request=UserRegisterSerializer,
    responses={
        status.HTTP_201_CREATED: TokenPairSerializer,
        status.HTTP_400_BAD_REQUEST: UserRegisterSerializer,
    },
    examples=[InvalidRegisterExample],
)
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token_pair_serializer = TokenPairSerializer(instance=user)
        return Response(data=token_pair_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Request user password reset via email",
    description="Send an email with a token to initiate the password reset process",
    responses={status.HTTP_200_OK: None},
)
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
                    "detail": "A reset password email had been sent to the provided email."
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data={
                    "detail": "A reset password email had been sent to the provided email."
                },
                status=status.HTTP_200_OK,
            )


@extend_schema(
    summary="Reset user password",
    description="Reset user password endpoint with token and user validation",
    responses={
        status.HTTP_200_OK: None,
        status.HTTP_400_BAD_REQUEST: ResetPasswordSerializer,
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
    },
    examples=[
        InvalidPasswordResetExample,
        UserNotFoundExample,
    ],
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


# TODO: Magic link authentication views
