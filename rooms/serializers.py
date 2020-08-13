from rest_framework import serializers
from .models import Room
from users.serializers import RelatedUserSerializer


class RoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

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
