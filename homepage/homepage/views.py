from django.shortcuts import render
import random

from siri.models import Forecast

def home(request):
    forecast = Forecast.objects.last()
    gradient = random.randint(0, 3)
    return render(request, "homepage/home.html", {
        "forecast": forecast,
        "gradient": gradient,
    })

def beta(request):
    forecast = Forecast.objects.last()
    gradient = random.randint(0, 3)
    return render(request, "homepage/home.html", {
        "forecast": forecast,
        "gradient": gradient,
        "beta": True
    })
