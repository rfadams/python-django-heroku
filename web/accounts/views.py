from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
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


class GroupDetailView(DetailView):
    template_name = 'generic/detail.html'

    def get_object(self):
        profile_username = self.kwargs.get('slug', None)

        if profile_username:
            user = User.objects.get(username=profile_username)
        else:
            user = self.request.user

        groups = user.member_of_group_set.all()
        if groups:
            return groups[0]
        else:
            return None


class GroupWithdrawView(FormView):
    template_name = 'generic/form.html'
    form_class = GroupWithdrawForm

    def form_valid(self, form):
        confirm_withdraw = form.cleaned_data.get('confirm_withdraw', False)

        if confirm_withdraw:
            user = self.request.user
            groups = user.member_of_group_set.all()
            
            if groups:
                groups[0].members.remove(user)

        return HttpResponseRedirect(reverse('accounts:profile'))


class GroupJoinView(FormView):
    template_name = 'generic/form.html'
    form_class = GroupJoinForm
    
    def get_form(self, form_class):
        return form_class(request=self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        user = self.request.user
        profile_username = self.kwargs.get('slug', None)

        if profile_username:
            group_member = User.objects.get(username=profile_username)
            group = group_member.member_of_group_set.all()[0]

            group.invites.add(user)
            
        return HttpResponseRedirect(reverse('accounts:user', kwargs={'slug': profile_username}))


class GroupJoinRequestsView(FormView):
    template_name = 'generic/form.html'
    form_class = GroupJoinRequestsForm

    def get_form(self, form_class):
        return form_class(self.request.user, **self.get_form_kwargs())
    
    def form_valid(self, form):
        requests = form.cleaned_data.get('requests', [])



        return HttpResponseRedirect('/account/group/requests')


