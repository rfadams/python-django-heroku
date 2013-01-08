from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='E-mail address')
    redirect_to = forms.CharField(required=False, initial='/profile/', widget=forms.HiddenInput)

class CreateUserForm(UserCreationForm):
    username = forms.EmailField(label='E-mail address')
    redirect_to = forms.CharField(required=False, initial='/profile/', widget=forms.HiddenInput)

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'username')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
