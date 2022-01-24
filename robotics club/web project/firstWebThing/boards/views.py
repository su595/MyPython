from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Bike
from datetime import datetime
import pytz

def bike_list(request):

    # instead of creating a background task (which I don't know how to do atm), we check for off campus bikes like this everytime someone views the main site 
    otherBikes = Bike.objects.all()
    for bike in otherBikes:
        bike.updateLastContactWithServer()

    bikes = Bike.objects.order_by("-onCampus") # order the bikes with off-campus-bikes at the bottom

        
    return render(request,"boards/bike_list.html", {"bikes": bikes})


def amIClaimed(request): # to be used by ESPs
    # this takes in a GET argument, and if that is a mac address that belongs to one of the bikes, the response will be t(rue) or f(alse) wheter that bike is claimed by someone

    myMA = request.GET.get("m", "")

    if myMA == "":
        return HttpResponse("This is an page for the bikes, not for humans!")
    if myMA == "test":
        return HttpResponse("everything works here")

    bike = Bike.objects.filter(macAddress=myMA).first() # this query should only ever have one result

    if bike is None:
        return HttpResponse("no valid bike macaddress :(")
    
    # now we know that a valid bike has accessed the /amIClaimed site

    # we can set the inWifi tag to True (most likely it already is true)
    bike.onCampus = True

    bike.lastContactWithServer = datetime.now(pytz.utc)

    bike.save()

    if bike.isClaimed:
        return HttpResponse("t")
    else:
        return HttpResponse("f")
    
    