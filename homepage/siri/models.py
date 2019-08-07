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
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Forecast` object is deleted.
    """
    if instance.audio:
        if os.path.isfile(instance.audio.path):
            os.remove(instance.audio.path)
