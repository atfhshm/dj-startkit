from rest_framework import serializers

# TODO: change the names to schema and example

__all__ = [
    "InvalidPassword",
]

InvalidPassword = {
    "password": ["Invalid password."],
    "new_password": [
        "Passwords missmatch.",
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric.",
    ],
}

InvalidUserUpdate = {
    "email": ["A user with that email already exists.", "Enter a valid email address."],
    "phone_number": ["A user with that phone number already exists."],
    "username": ["A user with that username already exists."],
}

UserNotFoundExample = {
    "detail": "User not found",
    "code": "user_not_found",
}


class UserNotFoundSchema(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()
