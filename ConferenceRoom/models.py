from django.db import models


class Rooms(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField(default=1)
    projector = models.BooleanField(default=False)


class Booking(models.Model):
    date = models.DateField(null=False)
    rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256, blank=True)

    class Meta:
        unique_together = ('date', 'rooms')
