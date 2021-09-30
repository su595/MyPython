from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Bike


def another(request):
    thisResponse = HttpResponse("test")
    thisResponse.content = "sfdsdsdg"
    return thisResponse

def bike_list(request):
    bikes = Bike.objects.order_by("inWifi")
    return render(request,"boards/bike_list.html", {"bikes": bikes})
    