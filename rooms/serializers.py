from rest_framework import serializers
from .models import Room
from users.serializers import TinyUserSerializer


class RoomSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer()

    class Meta:
        model = Room
        fields = (
            "name",
            "price",
            "instant_book",
            "user",
        )
