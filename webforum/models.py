from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils.text import Truncator


class Forum(models.Model):
	name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Topic(models.Model):
	subject = models.CharField(max_length=255)
	last_updated = models.DateTimeField(auto_now_add=True)
	forum = models.ForeignKey(Forum, related_name='topics')
	starter = models.ForeignKey(User, related_name='topics')
	views = models.PositiveIntegerField(default=0)
	def __str__(self):
		return self.subject

class Post(models.Model):
	message = models.TextField(max_length=4000)
	topic = models.ForeignKey(Topic, related_name='posts')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, related_name='posts')
	updated_by = models.ForeignKey(User, null=True, related_name='+')
	def __str__(self):
		truncate_message = Truncator(self.message)
		return truncate_message.char(30)