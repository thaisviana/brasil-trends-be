from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    size = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    second_round = models.BooleanField(default=False)
    top = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    election_year = models.IntegerField(default=2018)

    def __str__(self):
        return self.name
