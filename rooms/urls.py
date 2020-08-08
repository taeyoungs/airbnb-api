from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("list/", views.ListRoomsView.as_view()),
    path("<int:pk>", views.RoomDetailView.as_view()),
]
