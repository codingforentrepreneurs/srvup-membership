from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.text import Truncator

# Create your models here.
from accounts.models import MyUser
from videos.models import Video


class CommentManager(models.Manager):
	def all(self):
		return super(CommentManager, self).filter(active=True).filter(parent=None)

	def recent(self):
		try:
			limit_to = settings.RECENT_COMMENT_NUMBER
		except:
			limit_to = 6
		return self.get_queryset().filter(active=True).filter(parent=None)[:limit_to]

	def create_comment(self, user=None, text=None, path=None, video=None, parent=None):
		if not path:
			raise ValueError("Must include a path when adding a Comment")
		if not user:
			raise ValueError("Must include a user when adding a Comment")

		comment = self.model(
			user = user,
			path = path, 
			text = text
		)
		if video is not None:
			comment.video = video
		if parent is not None:
			comment.parent = parent
		comment.save(using=self._db)
		return comment


class Comment(models.Model):
	user = models.ForeignKey(MyUser)
	parent = models.ForeignKey("self", null=True, blank=True)
	path = models.CharField(max_length=350)
	video = models.ForeignKey(Video, null=True, blank=True)
	text = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	active = models.BooleanField(default=True)

	objects = CommentManager()

	class Meta:
		ordering = ['-timestamp']

	def __unicode__(self):
		return self.text


	def get_absolute_url(self):
		return reverse('comment_thread', kwargs={"id": self.id})

	@property 
	def get_origin(self):
		return self.path

	@property
	def get_preview(self):
		#return truncatechars(self.text, 120)
		return Truncator(self.text).chars(120)

	@property
	def get_comment(self):
		return self.text

	@property
	def is_child(self):
		if self.parent is not None:
			return True
		else:
			return False

	def get_children(self):
		if self.is_child:
			return None
		else:
			return Comment.objects.filter(parent=self)

	def get_affected_users(self):
		""" 
		it needs to be a parent and have children, 
		the children, in effect, are the affected users.
		"""
		comment_children = self.get_children()
		if comment_children is not None:
			users = []
			for comment in comment_children:
				if comment.user in users:
					pass
				else:
					users.append(comment.user)
			return users
		return None
















