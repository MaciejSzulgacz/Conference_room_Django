from django.db import models


class Rooms(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField(default=1)
    projector = models.BooleanField(default=False)
