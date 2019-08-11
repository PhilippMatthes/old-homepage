import os

from django.db import models
from django.dispatch import receiver
from django.utils.functional import cached_property

from siri.models import Readable
from ui.models import Renderable


class Artwork(Readable, Renderable):
    template_name = "art/artwork.html"

    file = models.FileField(upload_to="artworks/")
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.file.name

    @cached_property
    def extension(self):
        return os.path.splitext(self.file.name)[1].replace(".", "")

    @cached_property
    def is_video(self):
        endings = ["mkv", "mp4", "webm"]
        for ending in endings:
            if self.file.name.endswith(ending):
                return True
        return False

    def save(self, *args, **kwargs):
        if not self.description:
            self.is_ready = False
        if not self.readable_text and self.is_ready:
            self.readable_text = "{description}".format(
                description=self.description
            )
        super().save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Artwork)
def auto_delete_forecast_audio_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
