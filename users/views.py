from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReadUserSerializer, WriteUserSerializer
from .models import User


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
