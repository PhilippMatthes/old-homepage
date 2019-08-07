from django.db import models

from siri.models import Readable


class Service(Readable):
    title = models.TextField()
    description = models.TextField()

    icon_css = models.TextField(default="")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.readable_text:
            self.readable_text = "{description}".format(
                title=self.title, description=self.description
            )
        super().save(*args, **kwargs)