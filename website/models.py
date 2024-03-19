from django.db import models

class Workout(models.Model):
    registered_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    muscle_groups = models.CharField(max_length=100)