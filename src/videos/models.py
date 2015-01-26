import urllib2

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
# Create your models here.


class VideoQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True)


class VideoManager(models.Manager):
	def get_queryset(self):
		return VideoQuerySet(self.model, using=self._db)

	def get_featured(self, user, kabc=None):
		#Video.objects.get_featured(user, kabc="something")
		#Video.objects.filter(featured=True)
		#return super(VideoManager, self).filter(featured=True)
		return self.get_queryset().active().featured()

	def all(self):
		return self.get_queryset().active()


DEFAULT_MESSAGE = "Check out this awesome video."


class Video(models.Model):
	title = models.CharField(max_length=120)
	embed_code = models.CharField(max_length=500, null=True, blank=True)
	share_message = models.TextField(default=DEFAULT_MESSAGE)
	slug = models.SlugField(null=True, blank=True)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	free_preview = models.BooleanField(default=False)
	category = models.ForeignKey("Category", default=1)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)


	objects = VideoManager()

	class Meta:
		unique_together = ('slug', 'category')

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("video_detail", kwargs={"vid_slug": self.slug, "cat_slug": self.category.slug})

	def get_share_link(self):
		full_url = "%s%s" %(settings.FULL_DOMAIN_NAME, self.get_absolute_url())
		return full_url

	def get_share_message(self):
		full_url = "%s%s" %(settings.FULL_DOMAIN_NAME, self.get_absolute_url())
		return urllib2.quote("%s %s" %(self.share_message, full_url))


def video_post_save_receiver(sender, instance, created, *args, **kwargs):
	print "signal sent"
	if created:
		slug_title = slugify(instance.title)
		new_slug = "%s %s %s" %(instance.title, instance.category.slug, instance.id)
		try:
			obj_exists = Video.objects.get(slug=slug_title, category=instance.category)
			instance.slug = slugify(new_slug)
			instance.save()
			print "model exists, new slug generated"
		except Video.DoesNotExist:
			instance.slug = slug_title
			instance.save()
			print "slug and model created"
		except Video.MultipleObjectsReturned:
			instance.slug = slugify(new_slug)
			instance.save()
			print "multiple models exists, new slug generated"
		except:
			pass



post_save.connect(video_post_save_receiver, sender=Video)


class Category(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(max_length=5000, null=True, blank=True)
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	slug = models.SlugField(default='abc', unique=True)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("project_detail", kwargs={"cat_slug": self.slug})


TAG_CHOICES = (
	("python", "python"),
	("django", "django"),
	("css", "css"),
	("bootstrap", "bootstrap"),
)

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class TaggedItem(models.Model):
	#category = models.ForeignKey(Category, null=True)
	#video = models.ForeignKey(Video)
	tag = models.SlugField(choices=TAG_CHOICES)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	def __unicode__(self):
		return self.tag














