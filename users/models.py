from django.contrib.auth.models import AbstractUser
from django.db import models
from sortedm2m.fields import SortedManyToManyField
from rooms.models import Room


class User(AbstractUser):

    avatar = models.ImageField(upload_to="avatars", blank=True)
    superhost = models.BooleanField(default=False)
    favs = models.ManyToManyField("rooms.Room", related_name="favs")
    # favs = SortedManyToManyField(
    #     Room, blank=True, related_name="favs", sort_value_field_name="id"
    # )

    def room_count(self):
        return self.rooms.count()

    room_count.short_description = "Room Count"
