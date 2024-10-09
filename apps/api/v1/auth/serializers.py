from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import User

__all__ = [
    "TokenObtainPairSerializer",
    "TokenObtainPairResponseSerializer",
    "TokenRefreshResponseSerializer",
    "UserRegisterSerializer",
]


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6, required=True)


class TokenObtainPairSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128)


class TokensSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=132)
    refresh = serializers.CharField(max_length=132)


class TokenObtainPairResponseSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()
    phone_number = PhoneNumberField()

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
            "is_active",
            "date_joined",
            "updated_at",
            "tokens",
        )

    def get_tokens(self, obj) -> TokensSerializer:
        refresh = RefreshToken.for_user(obj)
        access = refresh.access_token

        return {"access": str(access), "refresh": str(refresh)}


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):
    """User Registeration Serializer"""

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
