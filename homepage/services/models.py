from django.db import models


class Service(models.Model):
    title = models.TextField()
    description = models.TextField()

    icon_css = models.TextField(default="")

    def __str__(self):
        return self.title