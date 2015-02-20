
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

from .signals import notify
# Create your models here.

class NotificationQuerySet(models.query.QuerySet):
	def get_user(self, recipient):
		return self.filter(recipient=recipient)

	def mark_targetless(self, recipient):
		qs = self.unread().get_user(recipient)
		qs_no_target = qs.filter(target_object_id=None)
		if qs_no_target:
			qs_no_target.update(read=True)

	def mark_all_read(self, recipient):
		qs = self.unread().get_user(recipient)
		qs.update(read=True)

	def mark_all_unread(self, recipient):
		qs = self.read().get_user(recipient)
		qs.update(read=False)

	def unread(self):
		return self.filter(read=False)

	def read(self):
		return self.filter(read=True)

	def recent(self):
		return self.unread()[:5]


class NotificationManager(models.Manager):
	def get_queryset(self):
		return NotificationQuerySet(self.model, using=self._db)

	def all_unread(self, user):
		return self.get_queryset().get_user(user).unread()

	def all_read(self, user):
		return self.get_queryset().get_user(user).read()

	def all_for_user(self, user):
		self.get_queryset().mark_targetless(user)
		return self.get_queryset().get_user(user)

	def get_recent_for_user(self, user, num):
		return self.get_queryset().get_user(user)[:num]


class Notification(models.Model):
	sender_content_type = models.ForeignKey(ContentType, related_name='nofity_sender')
	sender_object_id = models.PositiveIntegerField()
	sender_object = GenericForeignKey("sender_content_type", "sender_object_id")
	
	verb = models.CharField(max_length=255)

	action_content_type = models.ForeignKey(ContentType, related_name='notify_action', 
		null=True, blank=True)
	action_object_id = models.PositiveIntegerField(null=True, blank=True)
	action_object = GenericForeignKey("action_content_type", "action_object_id")

	target_content_type = models.ForeignKey(ContentType, related_name='notify_target', 
		null=True, blank=True)
	target_object_id = models.PositiveIntegerField(null=True, blank=True)
	target_object = GenericForeignKey("target_content_type", "target_object_id")

	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
	read = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	objects = NotificationManager()


	def __unicode__(self):
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = None
		context = {
			"sender": self.sender_object,
			"verb": self.verb,
			"action": self.action_object,
			"target": self.target_object,
			"verify_read": reverse("notifications_read", kwargs={"id": self.id}),
			"target_url": target_url,
		}
		if self.target_object:
			if self.action_object and target_url:
				return "%(sender)s %(verb)s <a href='%(verify_read)s?next=%(target_url)s'>%(target)s</a> with %(action)s" %context
			if self.action_object and not target_url:
				return "%(sender)s %(verb)s %(target)s with %(action)s" %context
			return "%(sender)s %(verb)s %(target)s" %context
		return "%(sender)s %(verb)s" %context
	
	@property	
	def get_link(self):
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = reverse("notifications_all")
		
		context = {
			"sender": self.sender_object,
			"verb": self.verb,
			"action": self.action_object,
			"target": self.target_object,
			"verify_read": reverse("notifications_read", kwargs={"id": self.id}),
			"target_url": target_url,
		}
		if self.target_object:
			return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s %(target)s with %(action)s</a>" %context
		else:
			return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s</a>" %context



def new_notification(sender, **kwargs):
	kwargs.pop('signal', None)
	recipient = kwargs.pop("recipient")
	verb = kwargs.pop("verb")
	#verb = kwargs["verb"]
	affected_users = kwargs.pop('affected_users', None)
	#print "affected users are"
	#print affected_users
	#print sender

	#target = kwargs.pop("target", None)
	#action = kwargs.pop("action", None)
	if affected_users is not None:
		for u in affected_users:
			if u == sender:
				pass
			else:
				print u
				new_note = Notification(
					recipient=u,
					verb = verb, # smart_text
					sender_content_type = ContentType.objects.get_for_model(sender),
					sender_object_id = sender.id,
					)
				for option in ("target", "action"):
					#obj = kwargs.pop(option, None)
					try:
						obj = kwargs[option]
						if obj is not None:
							setattr(new_note, "%s_content_type" %option, ContentType.objects.get_for_model(obj))
							setattr(new_note, "%s_object_id" %option, obj.id)
					except:
						pass
				new_note.save()
				print new_note
	else:
		new_note = Notification(
			recipient=recipient,
			verb = verb, # smart_text
			sender_content_type = ContentType.objects.get_for_model(sender),
			sender_object_id = sender.id,
			)
		for option in ("target", "action"):
			obj = kwargs.pop(option, None)
			if obj is not None:
				setattr(new_note, "%s_content_type" %option, ContentType.objects.get_for_model(obj))
				setattr(new_note, "%s_object_id" %option, obj.id)
		new_note.save()
		#print new_note


notify.connect(new_notification)

# justin  (AUTH_USER_MODEL)
# has commented ("verb")
# with a Comment (id=32) (instance action_object)
# on your Comment (id=12) (targeted instance)
# so now you should know about it (AUTH_USER_MODEL)

# <instance of a user>
# <something> #verb to 
# <instance of a model> #to
# <instance of a model> #tell
# <instance of a user>







