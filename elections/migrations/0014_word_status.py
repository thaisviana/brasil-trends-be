# Generated by Django 2.0.6 on 2018-07-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0013_auto_20180717_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]