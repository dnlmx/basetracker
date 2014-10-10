# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from bt.models.teams import Team
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile', unique=True)
	hours_per_week = models.DecimalField(verbose_name=_("Horas por semana"), max_digits=8, decimal_places=2, default=30)
	skype = models.CharField(verbose_name=_("Skype"), max_length=100, default='', blank=True)
	avatar = models.ImageField(verbose_name=_("Avatar"), upload_to='uploads/avatars', default='', blank=True)
	
	class Meta:
		app_label = 'bt'

	def __unicode__(self):
		return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
	"""Create the UserProfile when a new User is saved"""
	if created:
		profile = Profile()
		profile.user = instance
		profile.save()

post_save.connect(create_user_profile, sender=User)