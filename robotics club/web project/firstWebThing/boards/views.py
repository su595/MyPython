from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Bike
from .myFunctions import detect
from django.utils import timezone


def bike_list(request):

    bikes = Bike.objects.order_by("-onCampus") # order the bikes with off-campus-bikes at the bottom

    #if request.POST.get() is not None:
     #   pass
        
    return render(request,"boards/bike_list.html", {"bikes": bikes})


def amIClaimed(request): # to be used by ESPs
    # this takes in a GET argument, and if that is a mac address that belongs to one of the bikes, the response will be t(rue) or f(alse) wheter that bike is claimed by someone

    myMA = request.GET.get("m", "")
    print(myMA)

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

    # instead of creating a background task (which I don't know how to do atm), we check for off campus bikes like this regularly -> this only works with a lot of bikes connected 
    for bike in Bike.objects.all():
        bike.updateLastContactWithServer()

    bike.lastContactWithServer = timezone.now()

    if bike.isClaimed:
        return HttpResponse("t")
    else:
        return HttpResponse("f")
    