from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.forms import PasswordChangeForm

from accounts.forms import CreateUserForm, EditUserForm

from accounts.models import *

class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'generic/form.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        self.object = User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        founder = Founder(user=user)
        founder.save()

        return HttpResponseRedirect(reverse('accounts:profile'))


class EditUserView(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'generic/form.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:profile')


