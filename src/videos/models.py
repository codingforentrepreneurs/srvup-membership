from django.db import models
from django.core.urlresolvers import reverse
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


class Video(models.Model):
	title = models.CharField(max_length=120)
	embed_code = models.CharField(max_length=500, null=True, blank=True)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	free_preview = models.BooleanField(default=False)

	objects = VideoManager()

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("video_detial", kwargs={"id": self.id})
