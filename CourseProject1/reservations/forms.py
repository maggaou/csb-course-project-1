from django import forms
from reservations.models import Reservation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LogInForm(forms.Form):
  
    username = forms.CharField(max_length = 200)
    password = forms.CharField(max_length = 200)

    password = forms.CharField(widget = forms.PasswordInput())

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "date",
            "duration",
            "numberOfparticipants",
            "details",
            ]
        labels = {
            "date": "Date & Time",
            "duration": "Duration",
            "numberOfparticipants": "Participants",
            "details": "Details"
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2'
            ]
        # labels = {
        #     "username": "Name",
        #     "password1": "Password",
        #     "password2": "Password (again)",
        # }