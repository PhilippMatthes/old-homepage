from django.db import models


class Milestone(models.Model):
    title = models.TextField()
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title
