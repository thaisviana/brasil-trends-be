from django.db import models


class SizeHistory(models.Model):
    candidate = models.ForeignKey('Candidate', related_name='history', on_delete=models.CASCADE)
    date = models.DateTimeField()
    weekly_size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    haddad_weekly_size = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.candidate.name} - {self.date}'
