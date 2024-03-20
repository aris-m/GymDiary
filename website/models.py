from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    muscle_groups = models.CharField(max_length=100)

class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workouts = models.ManyToManyField(Workout)
    date = models.DateField()
    duration = models.IntegerField(null=True, blank=True)
    notes = models.TextField(max_length=200, null=True, blank=True)
    
class Goal(models.Model):
    workout = models.OneToOneField(Workout, on_delete=models.CASCADE, null=True, blank=True)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)