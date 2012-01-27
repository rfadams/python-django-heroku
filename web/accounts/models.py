import datetime
from django.db import models

from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify, capfirst


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

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.today()
        super(Activity, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Activity Log'


class Project(models.Model):
    creator = models.ForeignKey('auth.User')
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()
    url = models.URLField()

    modified    = models.DateTimeField(editable=False)
    created     = models.DateTimeField(editable=False)

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

    modified    = models.DateTimeField(editable=False)
    created     = models.DateTimeField(editable=False)

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
    creator = models.ForeignKey('auth.User', related_name='creator_of_groups', null=True)
    leader = models.ForeignKey('auth.User', related_name='leader_of_groups', null=True)
    members = models.ManyToManyField('auth.User', related_name='member_of_group_set')
    # invites = models.ManyToManyField('auth.User', blank=True, related_name='invites_of_group_set')

    def __unicode__(self):
        if self.leader:
            leader_username = self.leader.username
        else:
            leader_username = 'No leader'

        return capfirst(leader_username) + ' Group: ' + str([u.username for u in self.members.all()])



# class Achievement(models.Model):
#     pass

# class Goal(models.Model):
#     pass

# class PointRecord(models.Model):
#     pass

# class AttendanceRecord(models.Model):
#     pass
