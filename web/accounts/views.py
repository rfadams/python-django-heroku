from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.forms import PasswordChangeForm

from accounts.forms import *
from accounts.models import *
from util.models import *

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


class GroupSendInviteView(FormView):
    template_name = 'generic/form.html'
    form_class = GroupSendInviteForm

    def get_form(self, form_class):
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        cd = form.cleaned_data
        user = self.request.user
        receiver = cd.get('user', None)
        email = cd.get('email', None)
        invite = Invite()
        invite.sender = user

        if receiver:
            invite.receiver = receiver
        elif email:
            receiver = User.objects.create_user(email, email)
            invite.receiver = receiver

        groups = user.member_of_group_set.all()
        if groups:
            group = groups[0]
        else:
            group = Group()
            group.creator = user
            group.save()
            group.members.add(user)

        invite.group = group
        invite.save()

        return HttpResponseRedirect(reverse('accounts:group'))


def group_accept_invite_view(request, slug):
    invite = Invite.objects.get(slug=slug)
    sender = invite.sender
    receiver = invite.receiver
    group = invite.group
    user = request.user

    if user.is_authenticated():
        if not user.is_active:
            return HttpResponse('User account disabled. Sorry. Contact svsteam@svstartups.com')
        if user != receiver:
            return HttpResponse('This invite was not meant for you. If you think this is an error, contact svsteam@svstartups.com')
            
    #if new user
    if not receiver.has_usable_password():
        return HttpResponseRedirect(reverse('accounts:invite-newuser', kwargs={'slug': slug}))

    if invite.accepted or invite.declined:
        return HttpResponse('This invite has already been used. If you think this is an error, contact svsteam@svstartups.com')
    
    if request.method == 'POST':
        form = GroupAcceptInviteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            accept_invite = cd.get('accept_invite', False)
            decline_invite = cd.get('decline_invite', False)

            if accept_invite:
                group.members.add(user)
                invite.accepted = True
                invite.save()
                message = 'accepted the invite from <a href="%s">%s</a>.' % (reverse('accounts:user', kwargs={'slug': sender}), sender)
                url = reverse('accounts:group')
                
            
            if decline_invite:
                invite.declined = True
                invite.save()
                message = 'declined the invite from <a href="%s">%s</a>.' % (reverse('accounts:user', kwargs={'slug': sender}), sender)
                url = ''

            new_activity(user, message, receiver=sender, url=url, notification=True)
            new_activity(user, message, url=url)

            return HttpResponseRedirect(reverse('accounts:profile'))

    else:
        form = GroupAcceptInviteForm()

        if not invite.viewed:
            invite.viewed = True
            invite.save()

    return render_to_response('generic/form.html', {'form': form}, context_instance=RequestContext(request))
        

class GroupViewInviteNewUser(FormView):
    form_class = CreateUserForm
    template_name = 'generic/form.html'

    def get_success_url(self):
        return reverse('accounts:invite-newuser')

    def form_valid(self, form):
        cd = form.cleaned_data
        slug = self.kwargs.get('slug', '')
        invite = Invite.objects.get(slug=slug)
        receiver = invite.receiver

        receiver.username = cd['username']
        receiver.email = cd['email']
        receiver.set_password(cd['password1'])
        receiver.save()

        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        founder = Founder(user=user)
        founder.save()

        return HttpResponseRedirect(reverse('accounts:invite', kwargs={'slug': slug}))

# def point_reward_select_user_view(request):
#     if request.method == 'POST':
#         formset = PointRewardSelectUserForm(request.POST)

#         if formset.is_valid():
#             cd = formset.cleaned_data
#             for form in cd:
#                 point = Point()
#                 point.sender = request.user
#                 point.receiver = form['receiver']
#                 point.amount = form['amount']
#                 point.type = 2
#                 point.save()

#     else:
#         formset = PointRewardSelectUserForm()

#     return render_to_response('generic/form.html', {'form': formset}, context_instance=RequestContext(request))

class PointRewardView(CreateView):
    template_name = 'generic/form.html'

    def form_valid(self, form):
        cd = form.cleaned_data
        sender = cd['sender']
        receiver = cd['receiver']
        amount = cd['amount']

        point = Point()
        point.sender = sender
        point.receiver = receiver
        point.amount = amount
        point.type = 2
        point.save()

        sender_founder = cd['sender_founder']
        sender_founder.rewardable_points = sender_founder.rewardable_points - amount
        sender_founder.save()

        receiver_founder = cd['receiver_founder']
        receiver_founder.earned_points = receiver_founder.earned_points + amount
        receiver_founder.spendable_points = receiver_founder.spendable_points + amount
        receiver_founder.save()

        new_activity(sender, 'was rewarded points', receiver=receiver)

        return HttpResponseRedirect(self.get_success_url())
        

class PointRewardSelectUserView(PointRewardView):
    form_class = PointRewardSelectUserForm

    def get_form(self, form_class):
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def get_success_url(self):
        return reverse('accounts:profile')

class PointRewardUserView(PointRewardView):
    form_class = PointRewardUserForm

    def get_form(self, form_class):
        slug = self.kwargs.get('slug')
        receiver = User.objects.get(username=slug)
        sender = self.request.user
        return form_class(user=sender, receiver=receiver, **self.get_form_kwargs())
    
    def get_success_url(self):
        return reverse('accounts:user', kwargs={'slug': self.kwargs.get('slug')})

class PointListView(ListView):
    template_name = 'generic/list.html'

    def get_queryset(self):
        username = self.kwargs.get('slug') or self.request.user.username
        return Point.objects.filter(receiver__username=username)


