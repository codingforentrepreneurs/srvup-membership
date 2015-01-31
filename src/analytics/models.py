
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from .signals import page_view

class PageView(models.Model):
	path = models.CharField(max_length=350)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	primary_content_type = models.ForeignKey(ContentType, related_name='primary_obj',\
											null=True, blank=True)
	primary_object_id = models.PositiveIntegerField(null=True, blank=True)
	primary_object = GenericForeignKey("primary_content_type", "primary_object_id")

	secondary_content_type = models.ForeignKey(ContentType, related_name='secondary_obj',\
								null=True, blank=True)
	secondary_object_id = models.PositiveIntegerField(null=True, blank=True)
	secondary_object = GenericForeignKey("secondary_content_type", "secondary_object_id")

	timestamp = models.DateTimeField(default=timezone.now())

	def __unicode__(self):
		return self.path


def page_view_received(sender, **kwargs):
	kwargs.pop('signal', None)
	page_path = kwargs.pop('page_path')
	primary_obj = kwargs.pop('primary_obj', None)
	secondary_obj = kwargs.pop('secondary_obj', None)
	print secondary_obj
	user = sender
	if not user.is_authenticated():
		new_page_view = PageView.objects.create(path=page_path, timestamp=timezone.now())
	else:
		new_page_view = PageView.objects.create(path=page_path, user=user, timestamp=timezone.now())
	if primary_obj:
		new_page_view.primary_object_id = primary_obj.id
		new_page_view.primary_content_type = ContentType.objects.get_for_model(primary_obj)
		new_page_view.save()
	if secondary_obj:
		new_page_view.secondary_object_id = secondary_obj.id
		new_page_view.secondary_content_type = ContentType.objects.get_for_model(secondary_obj)
		new_page_view.save()



page_view.connect(page_view_received)