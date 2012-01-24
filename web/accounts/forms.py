from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from accounts.models import *

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm')

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('creator', 'slug')
        # exclude = ('slug',)
