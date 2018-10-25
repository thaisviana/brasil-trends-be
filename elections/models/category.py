from django.db import models


class Category(models.Model):
    text = models.CharField(max_length=255)
    ordering_factor = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.text

    class Meta:
        abstract = False
        ordering = ('ordering_factor',)