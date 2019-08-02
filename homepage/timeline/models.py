from django.db import models

class Milestone(models.Model):
    title = models.TextField()
    description = models.TextField()
    date = models.DateField()

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.title
