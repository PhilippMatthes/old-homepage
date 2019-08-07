import os

from django.db import models
from django.dispatch import receiver


class Forecast(models.Model):
    text = models.TextField()
    audio = models.FileField(upload_to="forecasts/")

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]


@receiver(models.signals.post_delete, sender=Forecast)
def auto_delete_forecast_audio_on_delete(sender, instance, **kwargs):
    if instance.audio:
        if os.path.isfile(instance.audio.path):
            os.remove(instance.audio.path)


class Readable(models.Model):
    readable_text = models.TextField(null=True, blank=True)
    readable_audio = models.FileField(upload_to="readables/", null=True, blank=True)


@receiver(models.signals.post_delete, sender=Readable)
def auto_delete_readable_audio_on_delete(sender, instance, **kwargs):
    if instance.readable_audio:
        if os.path.isfile(instance.readable_audio.path):
            os.remove(instance.readable_audio.path)
