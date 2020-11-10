import requests
import tempfile

from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.transaction import atomic
from django.utils import timezone

from siri.models import Forecast, Readable
from siri.synthesize import feed_forward


def get_weather_data():
    def deg_to_words(num):
        val=int((num/22.5)+.5)
        arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        for i, elem in enumerate(arr):
            arr[i] = elem.replace("N", " North").replace("S", " South").replace("W", " West").replace("E", " East")
        return arr[(val % 16)]

    # NOTE: removed old, invalidated api key
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Dresden&APPID=key&units=metric')
    weather_data = r.json()

    text = """Here is the current forecast of Dresden, Germany.
{main}. The temperature is currently at {temperature} degrees.
The wind is {wind_speed} kilometers per hour.
This data is fetched from openweathermap hourly. 
There might be some inaccuracies.""".format(
        date_str=timezone.now().strftime("%I %M %p"),
        main=weather_data["weather"][0]["main"].lower(),
        temperature=int(weather_data["main"]["temp"]),
        wind_speed=int(weather_data["wind"]["speed"]),
    ).strip()

    with tempfile.TemporaryDirectory() as tempdir:
        outfile_mp3 = feed_forward(text, str(tempdir))

        with open(outfile_mp3, 'rb') as f:
            audio = SimpleUploadedFile("forecast_{}.mp3".format(str(timezone.now())), f.read())
            Forecast.objects.create(text=text, audio=audio)

    with atomic():
        for forecast in list(Forecast.objects.all())[:-1]:
            forecast.delete()


def update_readables():
    for readable in Readable.objects.all():
        if readable.readable_audio:
            continue
        if not readable.is_ready:
            continue
        with tempfile.TemporaryDirectory() as tempdir:
            outfile_mp3 = feed_forward(readable.readable_text, str(tempdir))

            with open(outfile_mp3, 'rb') as f:
                readable.readable_audio = SimpleUploadedFile(
                    "readable_{}.mp3".format(readable.id), f.read()
                )
                readable.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_weather_data()
        update_readables()
