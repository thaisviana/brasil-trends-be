# Generated by Django 2.0.6 on 2018-09-24 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0019_auto_20180913_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='second_round',
            field=models.BooleanField(default=False),
        ),
    ]
