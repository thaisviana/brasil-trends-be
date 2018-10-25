from django.db import models


class SizeHistory(models.Model):
    candidate = models.ForeignKey('Candidate', related_name='history', null=True, blank=True, on_delete=models.SET_NULL)

    daily_size = models.PositiveIntegerField(default=1, null=True, blank=True)
    daily_real_size = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    weekly_size = models.PositiveIntegerField(default=1, null=True, blank=True)
    haddad_weekly_size = models.FloatField(default=1.0, null=True, blank=True)
    weekly_real_size = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    monthly_size = models.PositiveIntegerField(default=1, null=True, blank=True)
    monthly_real_size = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    yearly_size = models.PositiveIntegerField(default=1, null=True, blank=True)
    yearly_real_size = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    date = models.DateTimeField()
    #
    # def __str__(self):
    #     return self.candidate
