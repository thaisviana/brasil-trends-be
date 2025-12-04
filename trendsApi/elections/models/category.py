from django.db import models


class Category(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
