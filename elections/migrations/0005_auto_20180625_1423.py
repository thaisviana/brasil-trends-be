# Generated by Django 2.0.6 on 2018-06-25 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0004_auto_20180614_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='left',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='candidate',
            name='top',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
