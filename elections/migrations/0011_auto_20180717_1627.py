# Generated by Django 2.0.6 on 2018-07-17 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0010_auto_20180717_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sizehistory',
            name='real_size',
        ),
        migrations.RemoveField(
            model_name='sizehistory',
            name='size',
        ),
        migrations.AddField(
            model_name='sizehistory',
            name='daily_real_size',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sizehistory',
            name='daily_size',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='sizehistory',
            name='monthly_real_size',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sizehistory',
            name='monthly_size',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='sizehistory',
            name='weekly_real_size',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sizehistory',
            name='weekly_size',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='sizehistory',
            name='yearly_real_size',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sizehistory',
            name='yearly_size',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
