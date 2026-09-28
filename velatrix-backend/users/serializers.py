from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    security_answer = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "phone_number",
            "language_choice",
            "security_question",
            "security_answer",
        ]

    def create(self, validated_data):
        security_answer = validated_data.pop("security_answer")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.password = make_password(password)
        user.security_answer_hash = make_password(security_answer)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "phone_number",
            "birthday",
            "avatar",
            "country",
            "bio",
            "language_choice",
            "total_xp",
            "current_streak",
            "longest_streak",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "total_xp",
            "current_streak",
            "longest_streak",
            "created_at",
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class VerifySecurityAnswerSerializer(serializers.Serializer):
    username = serializers.CharField()
    security_answer = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
