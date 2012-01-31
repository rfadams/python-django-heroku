import datetime
from django.db import models

from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify, capfirst

from util import general

class Activity(models.Model):
    creator = models.ForeignKey('auth.User', related_name='activity_creator', db_index=True)
    receiver = models.ForeignKey('auth.User', related_name='activity_receiver', db_index=True, null=True)
    new = models.BooleanField(default=True, db_index=True)
    notification = models.BooleanField(default=False, db_index=True)
    message = models.CharField(max_length=200)
    url = models.CharField(max_length=200, blank=True)

    created = models.DateTimeField(editable=False)

    def __unicode__(self):
        receiver = self.receiver.username or 'Nobody'
        return '%s >> %s : %s' % (self.creator.username, receiver, self.message)
    
    def new_activity_record(self, user, message, *args, **kwargs):
        self.message = message

        self.creator = user
        self.receiver = user
        self.new = True
        self.notification = False
        self.url = ''

        for key, value in kwargs.items():
            self.__setattr__(key, value)
        
        super(Activity, self).save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        super(Activity, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['created']
        verbose_name_plural = 'Activity Log'


class Project(models.Model):
    creator = models.ForeignKey('auth.User')
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()
    url = models.URLField()

    modified = models.DateTimeField(editable=False)
    created = models.DateTimeField(editable=False)

    class Meta:
        ordering = ['-modified']

    def __unicode__(self):
        return self.name

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Project, self).save(*args, **kwargs)

    
class Founder(models.Model):
    user = models.ForeignKey('auth.User', unique=True)
    projects = models.ManyToManyField(Project, blank=True)
    earned_points = models.PositiveIntegerField(default=0)
    rewardable_points = models.PositiveIntegerField(default=0)
    spendable_points = models.PositiveIntegerField(default=0)

    modified = models.DateTimeField(editable=False)
    created = models.DateTimeField(editable=False)

    def __unicode__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Founder, self).save(*args, **kwargs)

    class Meta:
        ordering = ['user']


class Group(models.Model):
    creator = models.ForeignKey('auth.User', related_name='creator_of_groups', null=True, blank=True)
    leader = models.ForeignKey('auth.User', related_name='leader_of_groups', null=True, blank=True)
    members = models.ManyToManyField('auth.User', related_name='member_of_group_set')
    # invites = models.ManyToManyField('auth.User', blank=True, related_name='invites_of_group_set')

    def __unicode__(self):
        if self.leader:
            leader_username = self.leader.username
        else:
            leader_username = '_Leaderless'

        return capfirst(leader_username) + ' Group: ' + str([u.username for u in self.members.all()])

class Invite(models.Model):
<<<<<<< HEAD
    slug = models.SlugField(editable=False)
=======
    slug = models.SlugField()
>>>>>>> 2744d909d619c9de1ef28171ab4d0abcbbb316bb
    group = models.ForeignKey(Group, null=True)
    sender = models.ForeignKey('auth.User', related_name='sender_of_invite')
    receiver = models.ForeignKey('auth.User', related_name='receiver_of_invite')
    
    viewed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    modified = models.DateTimeField(editable=False)
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(general.get_random_string())
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Invite, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s - From: %s, To: %s' % (self.slug, self.sender, self.receiver) 

class Point(models.Model):
    point_types = (
        (1, 'earned'),
        (2, 'rewarded'),
        (3, 'spent'),
    )

    receiver = models.ForeignKey('auth.User', related_name='receiver_of_point')
    sender = models.ForeignKey('auth.User', related_name='sender_of_point', null=True)
    amount = models.IntegerField()
    type = models.PositiveSmallIntegerField(choices=point_types)

    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        super(Point, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s %d points' % (self.receiver, self.get_type_display(), self.amount)


# class Achievement(models.Model):
#     pass

# class Goal(models.Model):
#     pass

# class PointRecord(models.Model):
#     pass

# class AttendanceRecord(models.Model):
#     pass
