from datetime import date, time, timedelta
from os import name
from typing import Match
from django.db import models
from django.conf import settings
from datetime import datetime
import pytz # to make the datetime objects timezone aware and thus comparable
from firstWebThing import settings as mySettings 

# Create your models here.

class Bike(models.Model):


    macAddress = models.TextField(max_length=17)
    name = models.TextField(max_length=100)
    isClaimed = models.BooleanField(default=False)
    claimedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # this woudl be the key of the person claiming
    onCampus = models.BooleanField(default=True)
    size = models.TextField(max_length=1)
    needsRepair = models.BooleanField(default=False)
    lastContactWithServer = models.DateTimeField(datetime.now())

    def __str__(self) -> str:
        return self.name
    
    def updateLastContactWithServer(self):
        # if the last time the esp had contact with the server (through the amIClaimed website) is more than 80secs away, the bike is considered to be off campus
        now = datetime.now(pytz.utc)
        print(now - self.lastContactWithServer)

        if now - self.lastContactWithServer > timedelta(seconds=mySettings.BIKE_OFF_CAMPUS_TIME_LIMIT): # how to make this seconds??
            print(self.name + " bike off campus")
            self.onCampus = False
        
        self.save()



