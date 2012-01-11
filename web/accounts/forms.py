from django import forms
from django.contrib.auth.models import User

class NewUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)