from rest_framework import serializers
from .models import Room
from users.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_fields = (
            "user",
            "created",
            "updated",
            "id",
        )

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError(
                "Check-in and Check-out can't be set the same time"
            )
        return data

    def get_is_fav(self, obj):

        user = self.context.get("request").user
        if obj in user.favs.all():
            return True
        else:
            return False

    def create(self, validated_data):
        request = self.context.get("request")
        room = Room.objects.create(**validated_data, user=request.user)
        return room
