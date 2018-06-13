from django.db import models


class Word(models.Model):
    text = models.CharField(max_length=255)
    size = models.PositiveIntegerField(default=1)
