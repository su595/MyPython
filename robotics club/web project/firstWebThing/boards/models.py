from datetime import timedelta
from os import name
from typing import Match
from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Bike(models.Model):


    macAddress = models.TextField(max_length=17)
    name = models.TextField(max_length=100)
    isClaimed = models.BooleanField(default=False)
    claimedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # this woudl be the key of the person claiming
    onCampus = models.BooleanField(default=True)
    size = models.TextField(max_length=1)
    needsRepair = models.BooleanField(default=False)
    lastContactWithServer = models.TimeField(timezone.now())

    def __str__(self) -> str:
        return self.name
    
    def updateLastContactWithServer(self):
        # if the last time the esp had contact with the server (through the amIClaimed website) is more than 80secs away, the bike is considered to be off campus
        if timedelta(self.lastContactWithServer - timezone.now()) > timedelta(0, 80, 0): # how to make this seconds??
            self.onCampus = False


