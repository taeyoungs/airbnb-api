from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Room
from .serializers import RoomSerializer, BigRoomSerializer

# CBV
class ListRoomsView(ListAPIView):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(RetrieveAPIView):

    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer


# FBV
"""
@api_view(["GET"])
def list_rooms(request):
    rooms = Room.objects.all()
    serialized_rooms = RoomSerializer(rooms, many=True)
    return Response(data=serialized_rooms.data)
"""

