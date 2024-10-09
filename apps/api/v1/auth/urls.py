from django.urls import path

from .views import (
    TokenPairObtainView,
    TokenRefreshObtainView,
    UserRegisterView,
    VerifyTokenView,
)

urlpatterns = [
    path("register", UserRegisterView.as_view(), name="register-user"),
    path("tokens", TokenPairObtainView.as_view(), name="get-tokens"),
    path("tokens/refresh", TokenRefreshObtainView.as_view(), name="refresh-token"),
    path("tokens/verify", VerifyTokenView.as_view(), name="verify-token"),
]
