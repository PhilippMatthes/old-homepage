from django.db import models

from siri.models import Readable


class Milestone(Readable):
    title = models.TextField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.readable_text:
            self.readable_text = "{description}".format(
                title=self.title, description=self.description
            )
        super().save(*args, **kwargs)
