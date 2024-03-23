# Generated by Django 5.0.3 on 2024-03-23 14:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_remove_goal_workout_goal_workout_session_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="goal",
            name="reps",
        ),
        migrations.RemoveField(
            model_name="goal",
            name="sets",
        ),
        migrations.RemoveField(
            model_name="goal",
            name="weight",
        ),
        migrations.AddField(
            model_name="goal",
            name="accomplished",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="goal",
            name="description",
            field=models.TextField(default="No Description", max_length=200),
        ),
    ]
