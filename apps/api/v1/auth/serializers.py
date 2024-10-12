from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User

__all__ = [
    "TokenObtainPairSerializer",
    "TokenPairSerializer",
    "TokenSerializer",
    "InvalidTokenSerializer",
    "InvalidCredentialsSerializer",
    "TokenRefreshResponseSerializer",
    "UserRegisterSerializer",
    "RequestPasswordResetSerializer",
    "ResetPasswordSerializer",
]


class TokenObtainPairSerializer(serializers.Serializer):
    login = serializers.CharField(min_length=3, max_length=128)
    password = serializers.CharField(min_length=6, max_length=128)


class TokenPairSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=132)
    refresh = serializers.CharField(max_length=132)


class InvalidCredentialsSerializer(serializers.Serializer):
    detail = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, required=True)


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class InvalidTokenSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):
    """User Registration Serializer"""

    phone_number = PhoneNumberField()
    confirm_password = serializers.CharField(max_length=32)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "avatar",
            "password",
            "confirm_password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }

    def validate(self, attrs: dict):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                detail={"password": ["Passwords missmatch."]},
                code=status.HTTP_400_BAD_REQUEST,
            )
        email = attrs.get("email")
        if not email:
            raise serializers.ValidationError({"email": ["Email must be provided."]})

        return attrs

    def validate_password(self, value: str):
        if value:
            validate_password(value)
        return value

    def create(self, validated_data: dict) -> User:
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        email = validated_data.get("email")
        phone_number = validated_data.get("phone_number")
        avatar = validated_data.get("avatar")
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            phone_number=phone_number,
            avatar=avatar,
        )
        user.set_password(validated_data.get("password"))
        user.save()
        return user


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32)
    confirm_password = serializers.CharField(max_length=32)

    def validate(self, attrs: dict):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                detail={"password": ["Passwords missmatch."]},
                code=status.HTTP_400_BAD_REQUEST,
            )

        # Validate the password
        validate_password(password)
        validate_password(confirm_password)

        return attrs
