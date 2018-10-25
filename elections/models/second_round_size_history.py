from django.db import models


class SizeHistorySecondRound(models.Model):
    candidate = models.ForeignKey('Candidate', related_name='size_history_2', null=True, blank=True,
                                  on_delete=models.SET_NULL)

    size = models.PositiveIntegerField(default=1, null=True, blank=True)
    date = models.DateTimeField()
