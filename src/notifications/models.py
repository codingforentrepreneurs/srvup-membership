from django.db import models

from django.conf import settings
from .signals import notify
# Create your models here.


class Notification(models.Model):
	#sender = models.ForeignKey()
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
	action = models.CharField(max_length=255)
	#read
	#unread
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return str(self.action)



def new_notification(sender, recipient, action, *args, **kwargs):
	print recipient
	print action
	new_notification_create = Notification.objects.create(recipient=recipient, action=action)
	print sender
	print args
	print kwargs


notify.connect(new_notification)