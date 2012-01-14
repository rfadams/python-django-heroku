from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    username = forms.EmailField(label='E-mail address')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)