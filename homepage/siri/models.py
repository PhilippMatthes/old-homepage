from django.db import models

class Forecast(models.Model):
    text = models.TextField()
    audio = models.FileField(upload_to="forecasts/")

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
