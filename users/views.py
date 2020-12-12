import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from .serializers import UserSerializer
from .models import User
from .permissions import IsSelf
from rooms.models import Room
from rooms.serializers import RoomSerializer


class UsersViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        # print(self.action)
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "favs"
            or self.action == "token"
        ):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def token(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        if username is None or password is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "pk": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        rooms = user.favs.all()
        serializer = RoomSerializer(rooms, many=True, context={"request": request}).data

        return Response(data=serializer)

    @favs.mapping.put
    def toggle_favs(self, request, pk):

        pk = request.data.get("pk", None)
        # self.get_object() permission으로 이미 걸러져서 로그인한 유저의 favs만 넘어오는 구조
        user = self.get_object()

        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                print(room)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                Response(status=status.HTTP_404_NOT_FOUND)
        else:
            Response(status=status.HTTP_400_BAD_REQUEST)


# CBV
# Create Account
"""
class UsersView(APIView):
    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user).data
        return Response(data=serializer)

    def put(self, request):

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user).data
            return Response(data=user_serializer)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
"""

# FBV
"""
@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user).data
        return Response(data=serializer)
    except User.DoesNotExist:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def token(request):
    username = request.data.get("username", None)
    password = request.data.get("password", None)
    if username is None or password is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        encoded_jwt = jwt.encode(
            {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response(data={"token": encoded_jwt})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
"""
