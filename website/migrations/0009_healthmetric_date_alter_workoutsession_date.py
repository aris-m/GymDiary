# Generated by Django 5.0.3 on 2024-04-01 13:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0008_remove_calorieintake_user_healthmetric_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healthmetric",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="workoutsession",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]