from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.forms import PasswordChangeForm

from accounts.forms import *
from accounts.models import *

class CreateUserView(CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'generic/form.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        User.objects.create_user(username, email, password)
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


class CreateProjectView(CreateView):
    form_class = ProjectForm
    template_name = 'generic/form.html'

    def form_valid(self, form):
        user = self.request.user

        form.instance.creator = user
        project = form.save()
        project_url = reverse('accounts:project', kwargs={'username': user, 'slug': project.slug})

        founder = Founder.objects.get(user=user)
        founder.projects.add(project)

        activity = Activity()
        activity.creator = user
        activity.receiver = user
        activity.new = False
        activity.message = 'created a new project, <a href="%s">%s</a>!' % (project_url, project.name)
        activity.url = project_url
        activity.save()

        return HttpResponseRedirect(reverse('accounts:profile'))


class UpdateProjectView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'generic/form.html'

    def get_success_url(self):
        return reverse('accounts:project', kwargs={'username': self.request.user, 'slug': self.object.slug})
