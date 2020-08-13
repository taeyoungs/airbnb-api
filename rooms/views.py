from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer


# CBV
class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()[0:5]
        serializer = RoomSerializer(rooms, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def post(self, request):
        # 로그인 여부 확인
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):

        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(data=serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):

        room = self.get_room(pk)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if room is not None:
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                room = serializer.save(user=request.user)
                room_serializer = RoomSerializer(room).data
                return Response(data=room_serializer)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):

        room = self.get_room(pk)
        if room.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if room is not None:
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# FBV
"""
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
                room_serializer = ReadRoomSerializer(room).data
                return Response(data=room_serializer, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
"""
