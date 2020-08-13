from rest_framework import serializers
from .models import User


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "avatar", "superhost")


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
            "favs",
            "user_permissions",
        )


class WriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ()
