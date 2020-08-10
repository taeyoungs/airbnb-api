from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer


# FBV
@api_view(["GET", "POST"])
def list_rooms(request):
    if request.method == "GET":
        rooms = Room.objects.all()[0:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)
    elif request.method == "POST":
        # 로그인 여부 확인
        if request.user.is_authenticated:
            serializer = WriteRoomSerializer(data=request.data)
            if serializer.is_valid():
                room = serializer.save(user=request.user)
                return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# CBV
"""
class ListRoomsView(ListAPIView):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
"""


class RoomDetailView(RetrieveAPIView):

    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer

