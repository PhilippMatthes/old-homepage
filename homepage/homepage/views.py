from django.shortcuts import render

from siri.models import Forecast

def home(request):
    forecast = Forecast.objects.last()
    return render(request, "homepage/home.html", {
        "forecast": forecast
    })
