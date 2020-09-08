from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer
from .permissions import IsOwner


class RoomsViewSet(ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [AllowAny]
        elif self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):
        paginator = self.paginator

        filter_kwargs = {}

        max_price = request.GET.get("max_price", None)
        min_price = request.GET.get("min_price", None)
        beds = request.GET.get("beds", None)
        bedrooms = request.GET.get("bedrooms", None)
        bathrooms = request.GET.get("bathrooms", None)
        north = request.GET.get("north", None)
        south = request.GET.get("south", None)
        west = request.GET.get("west", None)
        east = request.GET.get("east", None)
        if max_price is not None:
            filter_kwargs["price__lte"] = max_price
        if min_price is not None:
            filter_kwargs["price__gte"] = min_price
        if beds is not None:
            filter_kwargs["beds__gte"] = beds
        if bedrooms is not None:
            filter_kwargs["bedrooms__gte"] = bedrooms
        if bathrooms is not None:
            filter_kwargs["bathrooms__gte"] = bathrooms
        if (
            north is not None
            and south is not None
            and west is not None
            and east is not None
        ):
            # print(north, south, west, east)
            filter_kwargs["lat__lte"] = float(north)
            filter_kwargs["lat__gte"] = float(south)
            filter_kwargs["lng__lte"] = float(east)
            filter_kwargs["lng__gte"] = float(west)

        try:
            rooms = Room.objects.filter(**filter_kwargs)
        except ValueError:
            rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(
            results, many=True, context={"request": request}
        ).data

        return paginator.get_paginated_response(data=serializer)


# CBV
"""
class OwnPagination(PageNumberPagination):
    page_size = 10

class RoomsView(APIView):
    def get(self, request):
        paginator = OwnPagination()
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(
            results, many=True, context={"request": request}
        ).data
        return paginator.get_paginated_response(data=serializer)

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
            serializer = RoomSerializer(room, context={"request": request}).data
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
"""

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
