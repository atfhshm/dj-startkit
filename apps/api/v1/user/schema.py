from rest_framework import status
from drf_spectacular.utils import OpenApiExample

__all__ = [
    "UserNotFoundExample",
    "InvalidPasswordExample",
    "InvalidUpdateUserExample",
]

UserNotFoundValues = {
    "detail": "User not found",
    "code": "user_not_found",
}
UserNotFoundExample = OpenApiExample(
    name="UserNotFound",
    response_only=True,
    status_codes=[status.HTTP_404_NOT_FOUND],
    value=UserNotFoundValues,
)

InvalidPasswordValues = {
    "password": ["Invalid password."],
    "new_password": [
        "Passwords missmatch.",
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric.",
    ],
}
InvalidPasswordExample = OpenApiExample(
    name="InvalidPassword",
    response_only=True,
    status_codes=[status.HTTP_400_BAD_REQUEST],
    value=InvalidPasswordValues,
)

InvalidUpdateUserValues = {
    "email": ["A user with that email already exists.", "Enter a valid email address."],
    "phone_number": ["A user with that phone number already exists."],
    "username": ["A user with that username already exists."],
}
InvalidUpdateUserExample = OpenApiExample(
    name="InvalidUserUpdate",
    value=InvalidUpdateUserValues,
    status_codes=[status.HTTP_400_BAD_REQUEST],
    response_only=True,
)
