from django.db import models


class Project(models.Model):
    thumbnail = models.ImageField(upload_to="projects/")
    title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title
