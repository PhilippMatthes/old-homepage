from django.db import models

from siri.models import Readable
from ui.models import Renderable


class Artwork(Readable, Renderable):
    template_name = "art/artwork.html"

    image = models.ImageField(upload_to="artworks/")
    title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.readable_text:
            self.readable_text = "{description}".format(
                title=self.title, description=self.description
            )
        super().save(*args, **kwargs)
