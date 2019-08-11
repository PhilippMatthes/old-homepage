from django.db import models

from siri.models import Readable
from ui.models import Renderable


class Artwork(Readable, Renderable):
    template_name = "art/artwork.html"

    image = models.ImageField(upload_to="artworks/")
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.description:
            self.is_ready = False
        if not self.readable_text and self.is_ready:
            self.readable_text = "{description}".format(
                description=self.description
            )
        super().save(*args, **kwargs)
