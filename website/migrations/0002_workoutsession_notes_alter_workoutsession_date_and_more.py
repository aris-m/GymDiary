# Generated by Django 5.0.3 on 2024-03-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="workoutsession",
            name="notes",
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="workoutsession",
            name="date",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="workoutsession",
            name="duration",
            field=models.DurationField(blank=True, null=True),
        ),
    ]
