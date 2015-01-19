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
		return reverse("category_detial", kwargs={"cat_slug": self.category.slug})









