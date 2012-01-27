from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError

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

class GroupWithdrawForm(forms.Form):
    confirm_withdraw = forms.BooleanField(label='Withdraw from group?')

class GroupJoinForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GroupJoinForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        user = self.request.user

        if user.member_of_group_set.count() > 0:
            raise ValidationError('You are already a member of a group')

        return self.cleaned_data


class GroupJoinRequestsForm(forms.Form):
     def __init__(self, user, *args, **kwargs):
        super(GroupJoinRequestsForm, self).__init__(*args, **kwargs)
        self.fields['requests'] = forms.ModelMultipleChoiceField(label='Requests to join group', queryset=Group.objects.filter(leader=user)[0].invites, widget=forms.CheckboxSelectMultiple)
