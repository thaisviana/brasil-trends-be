from django.db import models

PERIODS_CHOICES = (('TDY', 'today'),
                   ('WKK', 'week'),
                   ('MNT', 'month'),
                   ('YAR', 'year'),)


class Word(models.Model):
    text = models.CharField(max_length=255)
    size = models.PositiveIntegerField(default=1)
    period = models.CharField(max_length=255, choices=PERIODS_CHOICES, null=False, blank=False)
    candidate = models.ForeignKey('Candidate', related_name='words', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', related_name='words', null=True, blank=True, on_delete=models.SET_NULL)
