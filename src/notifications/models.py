
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .signals import notify
# Create your models here.


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
	
	#read
	#unread
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return str(self.verb)



def new_notification(sender, **kwargs):
	kwargs.pop('signal', None)
	recipient = kwargs.pop("recipient")
	verb = kwargs.pop("verb")
	#target = kwargs.pop("target", None)
	#action = kwargs.pop("action", None)
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
	print new_note


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







