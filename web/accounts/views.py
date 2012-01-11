from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

from web.accounts.forms import NewUserForm

class CreateUserView(FormView):
    form_class=NewUserForm
    template_name='generic/form.html'

    def form_valid(self, form, *args, **kwargs):
        username = email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = User.objects.create_user(username, email, password)
        user_auth = authenticate(username=username, password=password)
        login(self.request, user_auth)

        return HttpResponseRedirect(reverse('profile'))