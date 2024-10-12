from drf_spectacular.utils import OpenApiExample
from rest_framework import status

__all__ = [
    "InvalidAuthenticationExample",
    "InvalidTokenExample",
    "InvalidRegisterExample",
    "InvalidPasswordResetExample",
]
InvalidAuthenticationExample = OpenApiExample(
    name="InvalidCredentials",
    value={"detail": "Invalid credentials."},
    status_codes=[status.HTTP_401_UNAUTHORIZED],
    response_only=True,
)

InvalidTokenExample = OpenApiExample(
    name="InvalidToken",
    value={
        "detail": "Token is invalid or expired",
        "code": "token_not_valid",
    },
    status_codes=[status.HTTP_401_UNAUTHORIZED],
    response_only=True,
)

InvalidRegisterValues = {
    "first_name": ["This field is required."],
    "last_name": ["This field is required."],
    "email": ["A user with that email already exists.", "Enter a valid email address."],
    "phone_number": ["A user with that phone number already exists."],
    "password": [
        "Passwords missmatch.",
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric.",
    ],
}
InvalidRegisterExample = OpenApiExample(
    name="InvalidRegister",
    status_codes=[
        status.HTTP_400_BAD_REQUEST,
    ],
    value=InvalidRegisterValues,
    response_only=True,
)

InvalidPasswordResetValues = {
    "password": ["Invalid password.", "Passwords missmatch"],
    "confirm_password": [
        "Passwords missmatch.",
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric.",
    ],
}
InvalidPasswordResetExample = OpenApiExample(
    name="InvalidPasswordReset",
    value=InvalidPasswordResetValues,
    status_codes=[status.HTTP_400_BAD_REQUEST],
    response_only=True,
)
