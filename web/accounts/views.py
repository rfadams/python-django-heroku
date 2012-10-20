from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm 

from accounts.forms import CreateUserForm, EditUserForm
from util.models import *

class CreateUserView(DefaultsMixin, CreateView):
    model = User
    form_title = 'Create an Account'
    form_class = CreateUserForm
    template_name = 'generic/form.html'

    def form_valid(self, form):
        username = email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        self.object = User.objects.create_user(username, email, password)
        user_auth = authenticate(username=username, password=password)
        login(self.request, user_auth)

        return HttpResponseRedirect(reverse('accounts:profile'))


class EditUserView(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'generic/form.html'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        self.object.username = self.object.email = form.cleaned_data.get('email')
        self.object.save()

        return HttpResponseRedirect(reverse('accounts:profile'))

class LoginUserView(DefaultsMixin, FormView):
  form_title = 'Login'
  form_class = AuthenticationForm
  template_name = 'generic/form.html'

  def form_valid(self, form):
      username = email = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')

      user_auth = authenticate(username=username, password=password)
      login(self.request, user_auth)

      return HttpResponseRedirect(reverse('accounts:profile'))
