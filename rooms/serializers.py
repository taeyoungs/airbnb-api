from rest_framework import serializers


class RoomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    beds = serializers.IntegerField()
    instant_book = serializers.BooleanField()
