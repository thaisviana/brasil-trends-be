from django.db import models


class ImportantDates(models.Model):
    text = models.CharField(max_length=255)
    where = models.CharField(max_length=255)
    ref = models.CharField(max_length=255)
    date = models.DateTimeField()
    round = models.PositiveIntegerField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "{} no dia {}, {}".format(self.text, self.date, self.confirmed)