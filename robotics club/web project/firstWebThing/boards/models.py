from os import name
from typing import Match
from django.db import models
from django.conf import settings

# Create your models here.

class Bike(models.Model):


    macAddress = models.TextField(max_length=17)
    name = models.TextField(max_length=100)
    isClaimed = models.BooleanField(default=False)
    claimedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # this woudl be the key of the person claiming
    inWifi = models.BooleanField(default=True)
    size = models.TextField(max_length=1)
    needsRepair = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.name
