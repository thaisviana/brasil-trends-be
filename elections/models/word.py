from django.db import models

PERIODS_CHOICES = (('now 1-d', 'today'),
                   ('now 7-d', 'week'),
                   ('today 1-m', 'month'),
                   ('today 1-y', 'year'),)


class Word(models.Model):
    query_text = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    size = models.PositiveIntegerField(default=1)
    period = models.CharField(max_length=255, choices=PERIODS_CHOICES, null=False, blank=False)
    candidate = models.ForeignKey('Candidate', related_name='words', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', related_name='category_words', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)

    def __str__(self):
        return '%s , %s' % (self.text, self.candidate)

    class Meta:
        abstract = False
        ordering = ('-size',)