from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewTopicForm
from django.http import Http404
from .models import Forum, Topic, Post
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

def new_topic(request, pk):
	forum = get_object_or_404(Forum, pk=pk)
	user = User.objects.first()

	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.forum = forum
			topic.starter = user
			topic.save()
			post = Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by=user
			)
			return redirect('forum_topics', pk=forum.pk)
	else:
		form = NewTopicForm()
	return render(request, 'new_topic.html', {'forum': forum, 'form': form})
