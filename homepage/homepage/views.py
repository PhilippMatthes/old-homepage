from django.shortcuts import render
import random

from services.models import Service
from siri.models import Forecast

from ui.models import Gradient


def home(request):
    forecast = Forecast.objects.last()
    gradients = list(Gradient.objects.all())
    random.shuffle(gradients)
    gradient = gradients[0]
    return render(request, "homepage/home.html", {
        "forecast": forecast,
        "gradient": gradient,
        "gradients": gradients,
        "services": Service.objects.all()
    })
