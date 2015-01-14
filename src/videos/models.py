from django.db import models

# Create your models here.


class Video(models.Model):
	title = models.CharField(max_length=120)
	embed_code = models.CharField(max_length=500, null=True, blank=True)

	def __unicode__(self):
		return self.title
