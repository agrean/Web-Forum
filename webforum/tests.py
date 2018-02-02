from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from .views import home, forum_topics
from .models import Forum
# Create your tests here.
class HomeTests(TestCase):
	def setUP(self):
		self.forum = Forum.objects.create(name='Django', description='Django forum.')
		url = reverse('home')
		self.response = self.client.get(url)

	def test_home_view_status_code(self):
		self.assertEquals(response.status_code, 200)

	def test_home_url_resolve_home_view(self):
		view = resolve('/')
		self.assertEquals(view.func, home)

	def test_home_view_contains_link_to_topics_page(self):
		forum_topics_url = reverse('forum_topics', kwargs={'pk': self.forum.pk})
		self.assertContains(self.response, 'href="{0}"'.format(forum_topics_ur))

class ForumTopicsTests(TestCase):
	def setUp(self):
		Forum.objects.create(name='Django', description='This is Django Forum.')

	def test_forum_topics_view_success_status_code(self):
		url = reverse('forum_topics', kwargs={'pk': 1})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_forum_topics_view_not_found_status_code(self):
		url = reverse('forum_topics', kwargs={'pk': 99})
		response = self.client.get(url)
		self.assertEquals(response.status_code, 404)

	def test_forum_topics_url_resolve_forum_topics_view(self):
		view = resolve('/forums/1/')
		self.assertEquals(view.func, forum_topics)

	def test_forum_topics_view_contains_link_back_to_homepage(self):
        forum_topics_url = reverse('forum_topics', kwargs={'pk': 1})
        response = self.client.get(forum_topics_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))