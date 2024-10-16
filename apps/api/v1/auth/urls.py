from django.urls import path

from apps.api.v1.auth.views import (
    RequestPasswordResetView,
    ResetPasswordView,
    TokenPairObtainView,
    TokenRefreshObtainView,
    RegisterUserView,
    VerifyTokenView,
)

urlpatterns = [
    path(
        "tokens/register",
        RegisterUserView.as_view(),
        name="register-user",
    ),
    path(
        "tokens",
        TokenPairObtainView.as_view(),
        name="get-tokens",
    ),
    path(
        "tokens/refresh",
        TokenRefreshObtainView.as_view(),
        name="refresh-token",
    ),
    path(
        "tokens/verify",
        VerifyTokenView.as_view(),
        name="verify-token",
    ),
    path(
        "request-password-reset/",
        RequestPasswordResetView.as_view(),
        name="request-password-reset",
    ),
    path(
        "reset-password/<str:uidb64>/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset-password",
    ),
]
