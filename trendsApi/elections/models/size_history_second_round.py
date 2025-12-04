from django.db import models


class SizeHistorySecondRound(models.Model):
    candidate = models.ForeignKey('Candidate', related_name='history_second_round', on_delete=models.CASCADE)
    date = models.DateTimeField()
    size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.candidate.name} - {self.date}'
