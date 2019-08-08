import random

from django.db import models
from django.utils.functional import cached_property

from siri.models import Readable
from ui.models import Gradient


class Service(Readable):
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


class Technology(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title

    @cached_property
    def gradient(self):
        random.seed(self.title)
        return random.choice(list(Gradient.objects.all()))
