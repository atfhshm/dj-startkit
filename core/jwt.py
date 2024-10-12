from typing import TYPE_CHECKING

from rest_framework_simplejwt.tokens import RefreshToken

if TYPE_CHECKING:
    from apps.user.models import User

__all__ = [
    "get_tokens",
]


def get_tokens(user: "User") -> dict[str, str]:
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return {"access": str(access), "refresh": str(refresh)}
