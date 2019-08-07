import subprocess

import requests
import json
import datetime
import os
import wave
import tempfile

from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.transaction import atomic
from django.utils import timezone

from siri.models import Forecast
from siri.synthesize import feed_forward


def get_weather_data():
    def deg_to_words(num):
        val=int((num/22.5)+.5)
        arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        for i, elem in enumerate(arr):
            arr[i] = elem.replace("N", " North").replace("S", " South").replace("W", " West").replace("E", " East")
        return arr[(val % 16)]

    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dresden&APPID=234aa0e2c69010e09edd12b9f018ba8c&units=metric')
    weather_data = r.json()

    text = """Here is the current forecast of Dresden, Germany:
{main}. The temperature is currently at {temperature} degrees.
The wind is {wind_speed} kilometers per hour in direction {wind_direction}.
This data is fetched from openweathermap. There might be some inaccuracies.""".format(
        date_str=timezone.now().strftime("%I %M %p"),
        main=weather_data["weather"][0]["main"].lower(),
        temperature=weather_data["main"]["temp"],
        wind_speed=weather_data["wind"]["speed"],
        wind_direction=deg_to_words(int(weather_data["wind"]["deg"])),
    ).strip()

    with tempfile.TemporaryDirectory() as tempdir:
        outfile_path = feed_forward(text, str(tempdir))

        # Generate mp3 file with lame
        proc = subprocess.Popen(["lame", outfile_path])
        proc.communicate()

        with open(tempdir + "/output.mp3", 'rb') as f:
            audio = SimpleUploadedFile("forecast_{}.mp3".format(str(timezone.now())), f.read())
            Forecast.objects.create(text=text, audio=audio)

    with atomic():
        for forecast in list(Forecast.objects.all())[:-1]:
            forecast.delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_weather_data()
