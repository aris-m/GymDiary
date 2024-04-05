from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    CARDIO = 'Cardio'
    STRENGTH_TRAINING = 'Strength Training'
    BODYWEIGHT = 'Bodyweight'
    FLEX = 'Flexibility and Balance'
    OTHER = 'Other'

    TYPE_CHOICES = [
        (CARDIO, 'Cardio'),
        (STRENGTH_TRAINING, 'Strength Training'),
        (BODYWEIGHT, 'Bodyweight'),
        (FLEX, 'Flexibility and Balance'),
        (OTHER, 'Other'),
    ]
    
    CHEST = 'chest'
    BACK = 'back'
    ARMS = 'arms'
    ABDOMINALS = 'abdominals'
    LEGS = 'legs'
    SHOULDERS = 'shoulders'
    
    MUSCLE_GROUP_CHOICES = [
        (CHEST, 'chest'),
        (BACK, 'back'),
        (ARMS, 'arms'),
        (ABDOMINALS, 'abdominals'),
        (LEGS, 'legs'),
        (SHOULDERS, 'shoulders'),
    ]
    
    workout_session = models.ForeignKey('WorkoutSession', on_delete=models.CASCADE, related_name='session_workouts', default=None)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    muscle_groups = models.CharField(max_length=100)

class Goal(models.Model):
    workout_session = models.ForeignKey('WorkoutSession', on_delete=models.CASCADE, related_name='session_goals', default=None)
    description = models.TextField(max_length=200, default='No Description')
    accomplished = models.BooleanField(default=False)

class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workouts = models.ManyToManyField(Workout, related_name='sessions')
    goals = models.ManyToManyField(Goal, related_name='sessions')
    date = models.DateField(default=timezone.now)
    duration = models.IntegerField(null=True, blank=True)
    notes = models.TextField(max_length=200, null=True, blank=True)
    
class HealthMetric(models.Model):
    Kilogram = 'kg'
    Pound = 'lbs'
    
    UNITS = [
        (Kilogram, 'kg'),
        (Pound, 'lbs'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField(max_length=1000)
    unit = models.CharField(max_length=3)
    calories = models.FloatField(max_length=100000)
    date = models.DateField(default=timezone.now)
    
class FriendshipList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")