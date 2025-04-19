from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Reservation(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField() # Python datetime.date instance
    DURATION_CHOICES = {
        30: "30 min",
        45: "45 min",
        60: "60 min",
        90: "90 min"
    }
    duration = models.IntegerField(choices=DURATION_CHOICES, default=60)
    numberOfparticipants = models.IntegerField()
    details = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)