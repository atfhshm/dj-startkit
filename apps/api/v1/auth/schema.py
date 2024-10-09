__all__ = [
    "INVALID_USER_REGISTER_SCHEMA",
]

INVALID_USER_REGISTER_SCHEMA = {
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

invalid_password_object = {
    "password": ["Invalid password."],
    "new_password": [
        "Passwords missmatch.",
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric.",
    ],
}

invalid_password_reset_object = {
    "password": ["Invalid password."],
    "new_password": [
        "Passwords missmatch.",
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric.",
    ],
}
