# Generated by Django 2.0.6 on 2018-06-14 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0003_auto_20180613_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='candidate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='words', to='elections.Candidate'),
        ),
        migrations.AlterField(
            model_name='word',
            name='period',
            field=models.CharField(choices=[('now 1-d', 'today'), ('now 7-d', 'week'), ('today 1-m', 'month'), ('today 1-y', 'year')], max_length=255),
        ),
    ]
