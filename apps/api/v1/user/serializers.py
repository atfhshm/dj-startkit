from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "phone_number",
            "avatar",
            "date_joined",
            "updated_at",
            "last_login",
        )
        extra_kwargs = {
            "date_joined": {"read_only": True},
            "updated_at": {"read_only": True},
            "last_login": {"read_only": True},
        }


class PasswordChangeSerializer(serializers.ModelSerializer):
    """Change password serializer"""

    password = serializers.CharField(max_length=32)
    new_password = serializers.CharField(max_length=32)
    confirm_new_password = serializers.CharField(max_length=32)

    class Meta:
        model = User
        fields = ("password", "new_password", "confirm_new_password")
        read_only_fields = ("new_password", "confirm_new_password")

    def validate(self, attrs: dict):
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise serializers.ValidationError(
                detail={"new_password": ["Passwords missmatch."]},
                code=status.HTTP_400_BAD_REQUEST,
            )

        return attrs

    def validate_new_password(self, value):
        if value:
            validate_password(value)
        return value
