# Generated by Django 5.0.3 on 2024-04-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0006_alter_workout_muscle_groups_alter_workout_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bodyweight",
            name="unit",
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name="workout",
            name="muscle_groups",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="workout",
            name="type",
            field=models.CharField(max_length=50),
        ),
    ]
