# Generated by Django 2.0.6 on 2018-07-17 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0012_candidate_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sizehistory',
            name='daily_real_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sizehistory',
            name='daily_size',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='sizehistory',
            name='monthly_real_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sizehistory',
            name='monthly_size',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='sizehistory',
            name='weekly_real_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sizehistory',
            name='weekly_size',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='sizehistory',
            name='yearly_real_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='sizehistory',
            name='yearly_size',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]
