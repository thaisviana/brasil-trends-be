from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)
    size = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=10)
