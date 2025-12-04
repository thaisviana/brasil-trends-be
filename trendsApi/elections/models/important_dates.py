from django.db import models


class ImportantDates(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.text
