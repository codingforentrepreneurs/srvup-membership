from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
# Create your models here.


class Membership(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	date_end = models.DateTimeField(default=timezone.now(), verbose_name='End Date')
	date_start = models.DateTimeField(default=timezone.now(), verbose_name='Start Date')

	def __unicode__(self):
		return str(self.user.username)

	def update_status(self):
		if self.date_end >= timezone.now():
			self.user.is_member = True
			self.user.save()
		elif self.date_end < timezone.now():
			self.user.is_member = False
			self.user.save()
		else:
			pass


def update_membership_status(sender, instance, created, **kwargs):
	if not created:
		instance.update_status()


post_save.connect(update_membership_status, sender=Membership)