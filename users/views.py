from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReadUserSerializer, WriteUserSerializer
from .models import User
from rooms.models import Room
from rooms.serializers import RoomSerializer


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ReadUserSerializer(request.user).data
        return Response(data=serializer)

    def put(self, request):

        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = ReadUserSerializer(user).data
            return Response(data=user_serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        serializer = ReadUserSerializer(user).data
        return Response(data=serializer)
    except User.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        rooms = request.user.favs.all()
        serializer = RoomSerializer(rooms, many=True).data

        return Response(data=serializer)

    def put(self, request):

        pk = request.data.get("pk", None)
        user = request.user

        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                Response(status=status.HTTP_404_NOT_FOUND)
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)
