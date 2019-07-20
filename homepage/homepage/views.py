from django.shortcuts import render

def index(request):
    return render(request, "homepage/index.html")

def home(request):
    return render(request, "homepage/home.html")
