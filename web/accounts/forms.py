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


class GroupSendInviteForm(forms.Form):
    user = forms.CharField(label='Username', required=False)
    email = forms.EmailField(required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(GroupSendInviteForm, self).__init__(*args, **kwargs)

    def clean(self):
        cd = self.cleaned_data

        username = cd.get('user', None)
        email = cd.get('email', None)

        if not username and not email and not self.errors:
            raise ValidationError('Must send an invite to either a user or an email address')

        if username and email:
            raise ValidationError('Send an invite to either a user OR an email address, not both')

        groups = self.user.member_of_group_set.all()
        if groups and groups[0].members.count() >= 4:
            raise ValidationError('Your group is full. Send an email to svsteam@svstartups.com for instructions.')

        if username:
            user_query = User.objects.filter(username=username)
            if user_query:
                cd['user'] = user_query[0]
            else:
                raise ValidationError('No user has that username')
        elif email:
            email_query = User.objects.filter(email=email)
            if email_query:
                cd['user'] = email_query[0]

        return cd


class GroupAcceptInviteForm(forms.Form):
    accept_invite = forms.BooleanField(required=False)
    decline_invite = forms.BooleanField(required=False)

    def clean(self):
        cd = self.cleaned_data
        accept_invite = cd.get('accept_invite', False)
        decline_invite = cd.get('decline_invite', False)

        if accept_invite and decline_invite:
            raise ValidationError('Cannot both accept and decline the invite. Pick one.')
        
        if not accept_invite and not decline_invite:
            raise ValidationError('Please accept or decline the invite.')

        return cd

# class GroupViewInviteForm


# class GroupJoinForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super(GroupJoinForm, self).__init__(*args, **kwargs)
    
#     def clean(self):
#         user = self.request.user

#         if user.member_of_group_set.count() > 0:
#             raise ValidationError('You are already a member of a group')

#         return self.cleaned_data


# class GroupJoinRequestsForm(forms.Form):
#      def __init__(self, user, *args, **kwargs):
#         super(GroupJoinRequestsForm, self).__init__(*args, **kwargs)
#         self.fields['requests'] = forms.ModelMultipleChoiceField(label='Requests to join group', queryset=Group.objects.filter(leader=user)[0].invites, widget=forms.CheckboxSelectMultiple)
