from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    labels = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    size = models.FloatField(default=1)
    top = models.PositiveIntegerField(default=0)
    left = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    second_round = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = False
        ordering = ('-size',)
