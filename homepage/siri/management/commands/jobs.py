import requests
import json
import datetime
import os
import wave
import tempfile

from pydub import AudioSegment

from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
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

    text = """Here is the forecast of Dresden, Germany at {date_str}:
It is {main}. Temperatures peak from {temperature_min} to {temperature_max} degrees.
The wind is {wind_speed} kilometers per hour {wind_direction}.""".format(
        date_str = timezone.now().strftime("%I %M %p"),
        main = weather_data["weather"][0]["main"].lower(),
        temperature_min = weather_data["main"]["temp_min"],
        temperature_max = weather_data["main"]["temp_max"],
        wind_speed = weather_data["wind"]["speed"],
        wind_direction = deg_to_words(int(weather_data["wind"]["deg"])),
    ).strip()

    with tempfile.TemporaryDirectory() as tempdir:
        feed_forward(text, str(tempdir))
        infiles = [f for f in os.listdir(tempdir)]
        print(infiles)
        outfile = tempdir + "/forecast.wav"

        clip = AudioSegment.from_wav(tempdir + "/" + infiles[0])
        print(infiles[0])
        for infile in sorted(infiles[1:]):
            print(infile)
            clip += AudioSegment.from_wav(tempdir + "/" + infile)
        clip.export(outfile, format="wav")

        with open(outfile, 'rb') as f:
            audio = SimpleUploadedFile("forecast_{}.wav".format(str(timezone.now())), f.read())
            Forecast.objects.create(text=text, audio=audio)


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_weather_data()
