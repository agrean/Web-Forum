from django.shortcuts import render
from django.http import Http404
from .models import Forum
# Create your views here.

def home(request):
	forums = Forum.objects.all()
	return render(request, 'home.html', {'forums': forums})

def forum_topics(request, pk):
	try:
		forum = Forum.objects.get(pk=pk)
	except Forum.DoesNotExist:
		raise Http404
	return render(request, 'topics.html', {'forum': forum})