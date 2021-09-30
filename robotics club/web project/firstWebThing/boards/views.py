from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def another(request):
    thisResponse = HttpResponse("test")
    thisResponse.content = "sfdsdsdg"
    return thisResponse

def bike_list(request):
    bikes = 
    return render(request,"boards/bike_list.html", {})
    