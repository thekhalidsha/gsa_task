from django import forms
from django.contrib.auth.models import User


class UserRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']