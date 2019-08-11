from django.shortcuts import render
import random

from art.models import Artwork
from projects.models import Project
from services.models import Service, Technology
from siri.models import Forecast
from timeline.models import Milestone

from ui.models import Gradient


def home(request):
    gradients = list(Gradient.objects.all())
    random.shuffle(gradients)
    gradient = gradients[0]
    return render(request, "homepage/home.html", {
        "forecast": Forecast.objects.last(),
        "gradient": gradient,
        "gradients": gradients,
        "services": Service.objects.all(),
        "projects": Project.objects.all(),
        "milestones": Milestone.objects.all(),
        "technologies": Technology.objects.all(),
        "artworks": Artwork.objects.all().only("id"),
    })
