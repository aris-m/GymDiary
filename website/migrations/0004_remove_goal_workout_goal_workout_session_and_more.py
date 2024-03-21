# Generated by Django 5.0.3 on 2024-03-21 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0003_alter_workoutsession_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="goal",
            name="workout",
        ),
        migrations.AddField(
            model_name="goal",
            name="workout_session",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="session_goals",
                to="website.workoutsession",
            ),
        ),
        migrations.AddField(
            model_name="workout",
            name="workout_session",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="session_workouts",
                to="website.workoutsession",
            ),
        ),
        migrations.AddField(
            model_name="workoutsession",
            name="goals",
            field=models.ManyToManyField(related_name="sessions", to="website.goal"),
        ),
        migrations.AlterField(
            model_name="workoutsession",
            name="workouts",
            field=models.ManyToManyField(related_name="sessions", to="website.workout"),
        ),
    ]
